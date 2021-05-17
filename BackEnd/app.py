from flask      import Flask
from flask_cors import CORS

from BackEnd.view import create_endpoints
from BackEnd.service.user_service import TestService, UserService

class Services:
    pass

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    
    services = Services

###############초기세팅용#################
    services.test_service = TestService()
    services.user_service = UserService()
###############초기세팅용#################

    create_endpoints(app, services)

    return app