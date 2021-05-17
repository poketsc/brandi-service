from flask import jsonify

from BackEnd.model.user_dao import TestDao, UserDao
from BackEnd.util.exception import ValidationError
from BackEnd.util.message   import INVALID_NAME

#################################초기세팅#############################
class TestService:
    
    def test_service(self, data, connection):
        test_dao = TestDao()
            
        try:
            if len(data['size']) < 3:
                raise ValidationError(INVALID_NAME, 400)
            
            else:
                return test_dao.post_test(data, connection)

        except ValidationError as e:
            raise e

class UserService:
    def user_service(self, connection):
        user_dao = UserDao()

        results = user_dao.get_test(connection)

        return results

#################################초기세팅#############################