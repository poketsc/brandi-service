from flask      import Flask
from flask_cors import CORS

from BackEnd.view           import create_endpoints
from BackEnd.util.exception import CustomError

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})

    create_endpoints(app)

    @app.errorhandler(CustomError)
    def handle_errors(e):
        result = {'message' : e.message, 'status_code' : e.status_code}
    
        return result

    return app