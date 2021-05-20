from flask      import Flask, jsonify
from flask_cors import CORS

from view           import create_endpoints
from util.exception import CustomError
from util.message   import UNKNOWN_ERROR

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})

    create_endpoints(app)

    @app.errorhandler(CustomError)
    def handle_errors(e):
    
        return jsonify({'message' : e.message}), e.status_code

    @app.errorhandler(Exception)
    def handle_exceptions(e):
        
        return jsonify({'message' : UNKNOWN_ERROR}), 500
    
    return app