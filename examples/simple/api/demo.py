from ab.utils import logger
from ab.core import api
from ab import app
from ab.utils.rate_limit import rate_limit

# 可以使用这种方式载入配置里的数据，然后执行载入模型之类的操作
model_path = app.config.MODEL_PATH
logger.info('model path is:', model_path)


# 会自动暴露为/api/algorithm/add接口
@api()
@rate_limit(5)
def add(a: int, b: int) -> int:
    """
    一个简单的加法算法示例
    :param a: 第一个参数
    :param b: 第二个参数
    :return:
    """
    logger.info("enter algorithm {}, {} ".format(a, b))
    return a + b


@api()
def custom_response(a: int, b: int) -> int:
    """
    展示如何自定义响应体结构
    :param a: 第一个参数
    :param b: 第二个参数
    :return:
    """
    logger.info("enter algorithm {}, {} ".format(a, b))
    from flask import Response
    response = Response(f"Hello, {a - b}", status=200, mimetype='text/plain')
    return response

# @api()
# def crypto():
#     """
#     读取加密文件
#     :return:
#     """
#     from ab.keys.data import read_text, read_pickle, open_binary
#
#     # with open_binary("hanhao.pkl") as buffer:
#     #    print(1)
#     # return "aa"
#     return read_text("resource/mydata")
#     # return str(read_pickle("resource/hanhao"))[:20]
#
#
# @api()
# def compress() -> int:
#     """
#     :return:
#     """
#     return "this is a hello world text file, glad to meet you, bye ~this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye "
#
