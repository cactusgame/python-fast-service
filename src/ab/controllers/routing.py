from ab import jsonify
from ab import app
from ab.core import api_hub


@app.route('/routing', methods=['GET', 'POST'])
def routing():
    """
    :return: the table of `algorithm-name:service-name`
    """
    ret = dict()
    ret["service2algo"] = ["{}:{}".format(app.config["APP_NAME"], algo.name) for algo in api_hub.values()]
    ret["algo2service"] = ["{}:{}".format(algo.name, app.config["APP_NAME"]) for algo in api_hub.values()]
    return jsonify({'code': 0, 'data': ret})
