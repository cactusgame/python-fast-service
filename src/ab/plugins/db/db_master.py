"""
expose db as route
"""
from functools import partial, update_wrapper

from ab.utils.prometheus import http_metrics, time_metrics
from flask import request

from ab.plugins.db.dao import Mapper


mappers = {}


def get_mapper(key) -> Mapper:
    return mappers[key]

@http_metrics()
def list_page(mapper, list_columns, default_page_size, max_page_size):
    # TODO args order
    args = request.args.to_dict()
    page = int(args.pop('page', 1))
    size = int(args.pop('size', default_page_size))
    assert size <= max_page_size, 'page size must not exceed {max_page_size}'.format(max_page_size=max_page_size)
    order_by = args.pop('order_by', None)
    rows = mapper.select_page(fields=list_columns, conditions=args, order_by=order_by, page=page, size=size)
    count = mapper.count(conditions=args)
    from ab import jsonify
    return jsonify({"code": 0, "data": rows, "count": count})


@http_metrics()
def get_one_by_id(mapper, id, fields='*'):
    row = mapper.select_one_by_id(id, fields=fields)
    from ab import jsonify
    return jsonify({"code": 0, "data": row})


@http_metrics()
def add(mapper):
    row = request.get_json()
    row_id = mapper.insert(row)
    from ab import jsonify
    return jsonify({"code": 0, "data": row_id})


@http_metrics()
def update_one_by_id(mapper, id):
    row = request.get_json()
    ret = mapper.update_one_by_id(id, row)
    from ab import jsonify
    return jsonify({"code": 0, "data": ret})


@http_metrics()
def delete_one_by_id(mapper, id):
    ret = mapper.delete_one_by_id(id)
    from ab import jsonify
    return jsonify({"code": 0, "data": ret})