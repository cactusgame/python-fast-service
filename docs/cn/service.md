
# 自定义接口

## quick-start
在项目根目录的`api`目录下，为方法增加 @api注解即可。服务启动后，就可以用 /api/add 访问到服务了

```
from ab.utils import logger
from ab.utils.algorithm import algorithm
from ab import app

@api()
def add(a, b):
    logger.warning("enter algorithm {}, {} ".format(a, b))
    return a + b
```

# 接口格式

## 自定义返回格式
正常情况下，所有的接口默认返回`{"code": 0, "data": xxx}`这样的结构。

如果不想遵循这个格式，可以直接返回flask.Response对象，框架不会做任何处理。

## 返回二进制文件

```python
    from flask import make_response
    response = make_response(YOUR_CONTENT)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={YOUR_FILENAME}'
    return response
```

## 返回异常
1. 框架有一个默认异常类, 常见用法如下：

```python
from ab.utils.exceptions import AlgorithmException

try:
    1 / 0
except Exception as e:
    # from e必须要加，否则log会丢失异常栈，无法复现问题
    raise AlgorithmException(code=-100, data=YOUR_MSG) from e
```
则前端就会得到如下接口返回值：
```
{
    "code": -100,
    "data": YOUR_MSG
}
```

2. 如果抛出了未被捕获的异常，则前端接口会返回：
```
{
    "code": -1,
    "data": 异常堆栈
}
```

更多信息，详见 [异常与错误处理](error.md)



