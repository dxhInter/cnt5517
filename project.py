from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/things', methods=['POST'])
def create_thing():
    if not request.is_json:
        return jsonify({'code': 400, 'msg': 'No data provided'}), 400

    data = request.json
    print(data)
    return jsonify({'code': 200, 'msg': 'Thing created'}), 200


@app.route('/services', methods=['POST'])
def create_service():
    if not request.is_json:
        return jsonify({'code': 400, 'msg': 'No data provided'}), 400
    data = request.json
    print(data)
    return jsonify({'code': 200, 'msg': 'Service created'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)
