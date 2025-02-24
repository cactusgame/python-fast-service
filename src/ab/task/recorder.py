import datetime
import sys
import time
import traceback

from sqlalchemy.sql.functions import concat, coalesce

from ab.utils import logger
from ab.plugins.db import db_master

from ab import app
from ab.utils.mixes import chunk_string


class TaskRecorder:
    """
    the status will be updated to database
    """
    ERROR = -1
    INIT = 0
    RUNNING = 1
    DONE = 2

    @staticmethod
    def get_instance(task):
        return DbTaskRecorder(task)

    def log(self, *args, **kwargs):
        logger.debug('task: ', self.task.id, *args, **kwargs)

    def init(self, args):
        '''0: INIT'''
        self.log('init')
        return self.insert({'code': TaskRecorder.INIT})

    def concat_log(self, log: str, *args, **kwargs):
        # args && kwargs for print hook
        log += '\n'
        logger.debug(log)
        for s in chunk_string(log, 1000):
            return self.update({'log': concat(self.mapper.table.c.log, s)})

    def error(self, e: Exception):
        '''-1: ERROR'''
        st = traceback.format_exception(*sys.exc_info())
        logger.error('get async task error:', st)
        self.update({'code': TaskRecorder.ERROR, 'feature': {'msg': st}})
        if app.config.get('TESTING'):
            raise

    def done(self, result):
        '''2: DONE'''
        self.log('done')
        return self.update({'code': TaskRecorder.DONE, 'feature': result})

    """file-like object for hooking task stdout"""
    write = concat_log
    fileno = sys.__stdout__.fileno


class DummyTaskRecorder(TaskRecorder):
    def __init__(self, *args, **kwargs):
        pass

    def log(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def update_spark_app_id(self, *args, **kwargs):
        pass


class DbTaskRecorder(TaskRecorder):
    """
    persistently store records in rds
    """

    def __init__(self, task):
        self.task = task
        self.mapper = db_master.get_mapper('_task')

    def insert(self, mapping: dict):
        kwargs = mapping.copy()
        kwargs['task_id'] = self.task.id
        self.mapper.insert(kwargs)

    def update(self, mapping: dict):
        self.mapper.update(mapping, conditions={'task_id': self.task.id, 'gmt_modified': datetime.datetime.now()})
