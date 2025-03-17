#! python3
import sys
import traceback
from flask import request, Response
from io import BytesIO
from gzip import GzipFile

from ab.services import api_executor
from ab.utils import logger
from ab.utils.exceptions import AlgorithmException, Message

from ab import jsonify
from ab import app
from ab.utils.prometheus import http_metrics




@app.errorhandler(Exception)
def global_exception_handler(error):
    if app.config['TESTING']:
        # raise for pytest
        raise
    logger.exception()
    response = jsonify({'code': -1, 'data': "server error"})
    st = traceback.format_exception(*sys.exc_info())
    logger.error(st)
    try:
        response.status_code = error.code
    except:
        response.status_code = 500
    return response


@app.errorhandler(404)
def global_exception_handler(error):
    if app.config['TESTING']:
        # raise for pytest
        raise
    response = jsonify({'code': -1, 'data': '未找到页面'})
    response.status_code = error.code
    return response


@app.errorhandler(AlgorithmException)
def algorithm_exception_handler(error):
    if app.config['TESTING']:
        # raise for pytest
        raise
    response = jsonify({'code': error.code, 'data': error.data})
    logger.error(error.data)
    response.status_code = 500
    return response


@app.errorhandler(Message)
def algorithm_exception_handler(error):
    response = jsonify({'code': -100, 'data': error.msg})
    return response


@app.route('/', methods=['GET', 'POST'])
def health():
    return 'SUCCESS'

def convert_value(value):
    if not isinstance(value,str):
        return value

    # 尝试转换为布尔值
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'

    # 尝试转换为整数
    try:
        return int(value)
    except ValueError:
        pass

    # 尝试转换为浮点数
    try:
        return float(value)
    except ValueError:
        pass

    # 如果所有转换都失败，返回原始字符串
    return value


def multi_dict_to_flat_dict(mdict):
    """
    {(a, x), (b, y), (b, z)} -> {a: x, b: (y, z)}
    """
    ret = {}
    # https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.MultiDict
    for k in mdict:
        v = mdict.getlist(k)

        ret[k] = v[0] if len(v) == 1 else v
        ret[k] = convert_value(ret[k])
    return ret


def parse_algorithm_name(algorithm_name, response_format):
    if response_format == "gzip":
        return algorithm_name[:-4]
    else:
        return algorithm_name


def get_request_args(algorithm_name):
    body = {'args': {}}

    if request.is_json:
        body.update(request.get_json())
    if request.args:
        body['args'].update(multi_dict_to_flat_dict(request.args))

    if request.method == 'POST':
        if request.form:
            body['args'].update(multi_dict_to_flat_dict(request.form))
        if request.files:
            # bugfix: py3.5, d.update(request.files) get {k: [v]}, while py3.6 get {k: v}
            body['args'].update(multi_dict_to_flat_dict(request.files))

    # data source from config
    if app.config.FORCE_DATA_SOURCE and body.get('data_source'):
        logger.warning('config.FORCE_DATA_SOURCE is set, "data_source" in request body ignored')

    # parse response format
    f = request.path[-4:]
    if f == ".zip":
        body['format'] = "gzip"
    else:
        body['format'] = "identity"
    return body


def run_algorithm(request_body):
    result = api_executor.execute(request_body)
    if isinstance(result, Response):
        return result
    return jsonify({"code": 0, "data": result})


def run_algorithm_by_name(algorithm_name=None):
    body = get_request_args(algorithm_name)

    if algorithm_name:
        body['algorithm'] = parse_algorithm_name(algorithm_name, body["format"])
    return run_algorithm(body)


@app.route('/api/<string:api_name>', methods=['GET', 'POST'])
@http_metrics()  # must be decorated by @app.route
def run_algorithm_backend(api_name=None):
    """
    dataless api
    """
    return run_algorithm_by_name(api_name)


@app.after_request
def after_request_call(response):
    """
    todo: about the order of the handlers
    :return:
    """
    f = request.path[-4:]
    if f == ".zip":
        response.direct_passthrough = False
        gzip_buffer = BytesIO()
        with GzipFile(mode='wb',
                      compresslevel=6,
                      fileobj=gzip_buffer) as gzip_file:
            gzip_file.write(response.get_data())
        response.set_data(gzip_buffer.getvalue())

        response.headers['Content-Encoding'] = "gzip"
        response.headers['Content-Length'] = response.content_length

        etag = response.headers.get('ETag')
        if etag:
            response.headers['ETag'] = '{0}:{1}"'.format(etag[:-1], "gzip")

        vary = response.headers.get('Vary')
        if not vary:
            response.headers['Vary'] = 'Accept-Encoding'
        elif 'accept-encoding' not in vary.lower():
            response.headers['Vary'] = '{}, Accept-Encoding'.format(vary)
    else:
        pass
    return response

