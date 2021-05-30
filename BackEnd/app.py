import traceback

from datetime import datetime
from decimal import Decimal

from flask      import Flask, jsonify
from flask_cors import CORS
from flask.json                         import JSONEncoder
from flask_request_validator.exceptions import InvalidRequestError
from flask_request_validator.error_formatter import demo_error_formatter

from view           import create_endpoints
from util.exception import CustomError
from util.message   import UNKNOWN_ERROR


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, Decimal):
            return int(obj)
        return JSONEncoder.default(self, obj)


def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    CORS(app, resources={r"*": {"origins": "*"}})

    create_endpoints(app)

    @app.errorhandler(CustomError)
    def handle_errors(e):
        return jsonify({'message' : e.message}), e.status_code

    @app.errorhandler(InvalidRequestError)
    def handle_data_errors(e):
        return jsonify(demo_error_formatter(e)), 400

    @app.errorhandler(Exception)
    def handle_exceptions(e):
        traceback.print_exc()
        return jsonify({'message' : UNKNOWN_ERROR}), 500
    
    return app