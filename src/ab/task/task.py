import uuid
import os
from multiprocessing.pool import Pool
import time

from flask import Response
from prometheus_client import Gauge

from ab import app
from ab.utils import fixture, logger
from ab.core import ApiClass
from ab.utils.exceptions import AlgorithmException
from ab.plugins.data.engine import Engine
from ab.task.recorder import TaskRecorder


g_inprogress_async_tasks = Gauge("inprogress_async_tasks", "async task", labelnames=['mode'],
                                 multiprocess_mode='livesum')

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
        if request.get('mode', 'sync') == 'sync':
            return SyncTask(request)
        elif request['mode'] in ('async'):
            return PoolAsyncTask(request)
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

    def lazy_init(self):
        """
        heavy weight init
        """
        self.engine = Engine.get_instance(self.request.get('engine'))
        self.api = ApiClass.get_instance(self.request['algorithm'], self.engine._type)

        if 'task_id' in self.api.params:
            self.kwargs['task_id'] = self.id

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

    def __init__(self, request: dict):
        super().__init__(request)

        self.recorder = TaskRecorder.get_instance(task=self)
        self.recorder.init(self.kwargs)

    def inner_run(self):
        """
        lazy init, then run algorithm in another process
        """
        with g_inprogress_async_tasks.labels(mode=self.mode).track_inprogress():
            try:
                '''1. init'''
                logger.debug('async worker pid:', os.getpid())
                tic = time.time()
                self.lazy_init()
                toc = time.time()
                logger.debug('async lazy init time:', toc - tic)

                '''2. run'''
                result = self.run_algorithm()
                self.recorder.done(result)
            except Exception as e:
                self.recorder.error(e)
            finally:
                '''3. gc'''
                self.after_run()


class PoolAsyncTask(AsyncTask):
    """ process pool """
    pool = None
    mode = 'async_pool'

    @staticmethod
    def get_pool():
        """lazy init pool to avoid fork"""
        if PoolAsyncTask.pool:
            return PoolAsyncTask.pool

        pool_size = app.config.get('ASYNC_POOL_SIZE', 1)
        # two processes for each worker
        try:
            # setproctitle requires gcc, best effort
            # fixme: Mac OS after 10.2, can't fork process
            from setproctitle import setproctitle

            PoolAsyncTask.pool = Pool(processes=pool_size, initializer=lambda: setproctitle(
                'async pool for {ppid} [{app.config.APP_NAME}]'.format(ppid=os.getppid(), app=app)))
        except ImportError as e:
            PoolAsyncTask.pool = Pool(processes=pool_size)
        logger.debug('init async task pool:', PoolAsyncTask.pool, '\n')
        return PoolAsyncTask.pool

    def run(self):
        # When an object is put on a queue, the object is pickled (by pickle.dumps) and
        # a background thread later flushes the pickled data to an underlying pipe.
        # This has some consequences which are a little surprising, but should not cause any practical difficulties
        pool = self.get_pool()
        pool.apply_async(self.inner_run)

        return self.id
