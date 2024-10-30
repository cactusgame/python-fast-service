#! python3
import sys
import traceback
from ab.const import ErrorCode


class AlgorithmException(Exception):
    """
    base exception for algorithms
    """

    def __init__(self, code=-1, data=None):
        super(AlgorithmException, self).__init__(data)

        self.code = code
        extra = data if data is not None else ""
        self.data = ErrorCode.get_description(code) + extra
        # traceback.format_exception(*sys.exc_info()))
        if code == -1 and data is None:
            self.data = traceback.format_exception(*sys.exc_info())


class ConfigException(AlgorithmException):
    """
    exception for ab configs
    """
    pass


class RemoteAPIException(AlgorithmException):
    """
    exception for spring cloud interface invocation
    """
    pass


class DuplicatedKeyException(AlgorithmException):
    def __init__(self, data=None):
        super(DuplicatedKeyException, self).__init__(-2, data)


class DataAPIException(AlgorithmException):
    def __init__(self, data=None):
        super(DataAPIException, self).__init__(-10, data)


class Message(Exception):
    def __init__(self, msg):
        self.msg = msg
