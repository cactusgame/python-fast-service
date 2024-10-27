# coding: utf-8


from ab.core import algorithm


@api()
def sync():
    return "hello-sync-task"


@api()
def async_unlimit():
    import time
    time.sleep(2)
    return "hello-async-unlimit-task"


@api()
def async_pool():
    import time
    time.sleep(2)
    return "hello-async-pool-task"
