from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS
import service.service as service

app = Flask(__name__)
CORS(app)


# to check if the request is json
def check_json_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'code': 400, 'msg': 'No data provided'}), 400
        return f(*args, **kwargs)

    return decorated_function


@app.route('/things', methods=['POST'])
@check_json_request
def create_thing():
    result = service.create_thing(request.json)
    return jsonify(result), result['code']


@app.route('/things/<thing_id>', methods=['GET'])
def query_service_with_thing(thing_id):
    result = service.query_service_with_thing(thing_id)
    return jsonify(result), result['code']


@app.route('/services', methods=['POST'])
@check_json_request
def create_service():
    result = service.create_service(request.json)
    return jsonify(result), result['code']


@app.route('/services', methods=['GET'])
def query_all_services():
    result = service.query_all_services()
    return jsonify(result), result['code']


@app.route('/relationships', methods=['POST'])
@check_json_request
def create_relationship():
    result = service.create_relationship(request.json)
    return jsonify(result), result['code']


@app.route('/relationships', methods=['GET'])
def query_all_relationships():
    result = service.query_all_relationships()
    return jsonify(result), result['code']


@app.route('/apps', methods=['POST'])
@check_json_request
def create_app():
    result = service.create_app(request.json)
    return jsonify(result), result['code']


@app.route('/apps/<app_id>', methods=['GET'])
def get_app(app_id):
    result = service.get_app(app_id)
    return jsonify(result), result['code']


@app.route('/apps', methods=['GET'])
def query_all_apps():
    result = service.query_all_apps()
    return jsonify(result), result['code']


@app.route('/apps/run', methods=['POST'])
@check_json_request
def run_app():
    result = service.run_app(request.json)
    return jsonify(result), result['code']


@app.route('/apps/startOrStop', methods=['POST'])
@check_json_request
def start_or_stop_app():
    result = service.start_or_stop_app(request.json)
    return jsonify(result), result['code']

@app.route('/apps/delete/<app_id>', methods=['GET'])
def delete_app(app_id):
    result = service.delete_app(app_id)
    return jsonify(result), result['code']

@app.route('/apps/threshold', methods=['POST'])
def put_threshold():
    if not request.is_json:
        return jsonify({'code': 400, 'msg': 'No data provided'}), 400
    data = request.json
    result = service.put_threshold(data)
    return jsonify(result), result['code']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
