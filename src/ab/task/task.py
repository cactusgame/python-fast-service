import uuid

from flask import Response
from multiprocessing import Process
from multiprocessing.pool import Pool

import os
import time

from ab.core import ApiClass
from ab.utils.exceptions import AlgorithmException
from ab.plugins.data.engine import Engine
from ab.task.recorder import TaskRecorder
from ab.utils import logger, fixture
from ab import app
from ab.plugins.cache.redis import cache_plugin

class Task:
    """
    stateful algorithm runner
    """

    @staticmethod
    def get_next_id():
        """
        docker uses the IPv4 address of the container to generate MAC address
        which may lead to a collision
        just use the random uuid version 4
        """
        return uuid.uuid4().hex

    @staticmethod
    def get_instance(request):
        # run in sync mode as default
        mode = request.get('mode', 'sync')
        if mode == 'sync':
            return SyncTask(request)
        elif mode == 'async':
            return PoolAsyncTask(request)
        elif mode == 'async_unlimited':
            return UnlimitedAsyncTask(request)
        else:
            raise AlgorithmException('unknown mode:', request['mode'])

    def __init__(self, request: dict):
        """
        light weight init.
        the whole self object should be dumpable after init since AsyncTask.run depends on pickle.dumps
        """
        self.engine = None
        self.api = None
        self.id = Task.get_next_id()
        self.request = request
        if 'args' in self.request:
            self.kwargs = self.request['args'].copy()
        else:
            self.kwargs = {}
        self.recorder = TaskRecorder.get_instance(task=self)
        self.recorder.init(self.kwargs)

    def lazy_init(self):
        """
        heavy weight init
        """
        self.engine = Engine.get_instance(self.request.get('engine'))
        self.api = ApiClass.get_instance(self.request['algorithm'], self.engine._type)

        if 'cache_client' in self.api.params:
            self.kwargs['cache_client'] = cache_plugin.get_cache_client()

        if 'task_id' in self.api.params:
            self.kwargs['task_id'] = self.id

        if 'recorder' in self.api.params:
            self.kwargs['recorder'] = self.recorder

        used_fixtures = set(self.api.params) & fixture.fixtures.keys()
        for f in used_fixtures:
            ret = fixture.fixtures[f].run(self.request, self.kwargs)
            if ret is not None:
                if f in self.kwargs and not fixture.fixtures[f].overwrite:
                    raise AlgorithmException(data='fixture try to overwrite param {f}'.format(f=f))
                self.kwargs[f] = ret

        # TODO auto type-conversion according to type hint

    def run_api(self):
        result = self.api.run(self.kwargs)
        if isinstance(result, Response):
            return result

        return result
        # return {
        #     'result': result
        # }

    def after_run(self):
        self.engine.stop()

    def run(self):
        raise Exception('must be implemented')


class SyncTask(Task):
    def run(self):
        try:
            '''1. init'''
            self.lazy_init()
            '''2. run'''
            ret = self.run_api()
            return ret
        finally:
            '''3. gc'''
            self.after_run()


class AsyncTask(Task):

    def inner_run(self):
        """
        lazy init, then run algorithm in another process
        """
        try:
            '''1. init'''
            logger.debug('async worker pid:', os.getpid())
            tic = time.time()
            self.lazy_init()
            toc = time.time()
            logger.debug('async lazy init time:', toc - tic)

            '''2. run'''
            result = self.run_api()
            self.recorder.done(result)
        except Exception as e:
            self.recorder.error(e)
        finally:
            '''3. gc'''
            self.after_run()


class UnlimitedAsyncTask(AsyncTask):
    """create new process for each task"""
    mode = 'async_unlimited'

    def run(self):
        """
        it doesn't fork all memory on MAC
        :return:
        """
        p = Process(target=self.inner_run)
        p.start()

        return self.id


class PoolAsyncTask(AsyncTask):
    """
    process pool
    notice: it may only work on Linux
    """
    pool = None

    @staticmethod
    def get_pool():

        """lazy init pool to avoid fork"""
        if PoolAsyncTask.pool:
            return PoolAsyncTask.pool

        pool_size = app.config.get('ASYNC_POOL_SIZE', 2)

        PoolAsyncTask.pool = Pool(processes=pool_size)
        return PoolAsyncTask.pool

    def run(self):
        pool = self.get_pool()
        pool.apply_async(self.inner_run)
        return self.id
