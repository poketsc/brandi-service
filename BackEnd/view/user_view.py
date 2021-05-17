from flask import request, jsonify
from flask.views import MethodView

from BackEnd.connection import connect_db

###################################초기세팅############################
class TestView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        connection = None
        try:
            connection = connect_db()
            
            data = request.json
            
            results = self.service.test_service(data, connection)
            
            connection.commit()
            
            return jsonify({'results' : results})
            
        finally:
            if connection is not None:
                connection.close()
    
    def get(self):
        connection = None
        try:
            connection = connect_db()
            
            results = self.service.user_service(connection)
            
            connection.commit()
            
            return jsonify({'results' : results})
            
        finally:
            if connection is not None:
                connection.close()
###################################초기세팅############################
