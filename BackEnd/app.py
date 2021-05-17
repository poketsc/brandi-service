from flask      import Flask
from flask_cors import CORS

from view import create_endpoints

class Services:
    pass

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    
    services = Services

    create_endpoints(app, services)

    return app