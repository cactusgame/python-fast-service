"""
register the endpoint
"""

from ab.endpoint.registry import register_endpoint

# todo: move to config
register_endpoint('/api/document/<string:api_name>')
