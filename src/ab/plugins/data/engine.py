from ab.utils import logger
from ab.utils.exceptions import AlgorithmException


class Engine:
    @staticmethod
    def get_instance(config: dict = None):
        if not config or config['type'] == 'python':
            return Engine('python')

    def __init__(self, _type):
        self._type = _type
        pass

    def stop(self):
        pass


