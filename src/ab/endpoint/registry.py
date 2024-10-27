from ab import jsonify
from ab import app
from ab.utils.prometheus import http_metrics


# @app.route('/api/document/<string:algorithm_name>', methods=['GET', 'POST'])
# @http_metrics()  # must be decorated by @app.route
# def api_document(algorithm_name=None):
#     from ab.controllers.algorithm import run_algorithm_by_name
#     return run_algorithm_by_name(algorithm_name)

# @app.route('/api/document/<string:algorithm_name>', methods=['GET', 'POST'])
# @http_metrics()  # must be decorated by @app.route
def register_endpoint(rule):
    route = app.route(rule, methods=['GET', 'POST'])

    def api_document(api_name=None):
        from ab.controllers.algorithm import run_algorithm_by_name
        return run_algorithm_by_name(api_name)

    return route(api_document)
