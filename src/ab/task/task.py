import uuid

from flask import Response

from ab.utils import fixture
from ab.core import ApiClass
from ab.utils.exceptions import AlgorithmException
from ab.plugins.data.engine import Engine
from ab.task.recorder import TaskRecorder


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
