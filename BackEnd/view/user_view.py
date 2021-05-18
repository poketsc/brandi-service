from flask       import request, jsonify
from flask.views import MethodView

from service.user_service import TestService, UserService
from connection           import connect_db

###################################초기세팅############################
class TestView(MethodView):

    def post(self):
        test_service = TestService()

        connection = None
        try:
            connection = connect_db()
            
            data = request.json
            
            results = test_service.test_service(data, connection)
            
            connection.commit()
            
            return jsonify({'results' : results})
        
        except Exception as e:
            connection.rollback()
        
            raise e 
            
        finally:
            if connection is not None:
                connection.close()
    
    def get(self):
        user_service = UserService()
        connection = None
        try:
            connection = connect_db()
            
            results = user_service.user_service(connection)
            
            connection.commit()
            
            return jsonify({'results' : results})
            
        finally:
            if connection is not None:
                connection.close()
###################################초기세팅############################
