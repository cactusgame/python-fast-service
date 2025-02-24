from collections import OrderedDict
from ab.utils.prometheus import http_metrics
from ab.plugins.db.db_master import get_mapper
from flask import request
from ab import app, jsonify

mapper = get_mapper('_task')

@app.route('/api/task/<string:task_id>', methods=['GET'])
@http_metrics()  # must be decorated by @app.route
def get_task_by_id(task_id):
    # row = mapper.select_one_by_id(task_id, fields=['id','task_id','code','feature','gmt_create','gmt_modified'])
    row = mapper.select_one_by_id(task_id)
    return jsonify(row)