from ab.core import algorithm
from ab.utils.exceptions import Message


@api('exception')
def exception():
    return 1 / 0


@api('msg')
def msg():
    raise Message('hello world')
