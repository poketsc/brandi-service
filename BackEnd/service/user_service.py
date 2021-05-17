from flask import jsonify

from BackEnd.model.user_dao import TestDao, UserDao
from BackEnd.util.exception import ValidationError

#################################초기세팅#############################
class TestService:
    
    def test_service(self, data, connection):
        test_dao = TestDao()
            
        if len(data['name']) < 3:
            raise ValidationError('message', 400)
            
        else:
            results = test_dao.post_test(data, connection)

            return results

class UserService:
    def user_service(self, connection):
        user_dao = UserDao()

        results = user_dao.get_test(connection)

        return results

#################################초기세팅#############################