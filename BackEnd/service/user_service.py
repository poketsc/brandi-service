import bcrypt, jwt

from model.user_dao import SignInDao
from util.exception import InvalidRequest
from util.message   import WRONG_ID_OR_PW
from config         import SECRET_KEY, ALGORITHM

class SignInService:
    def post_sign_in(self, connection, data):
        sign_in_dao = SignInDao()

        try:
            user_info = sign_in_dao.get_user_info(connection, data)
            
            # 데이터베이스에 nickname이 존재하지 않으면 에러 처리.
            if not user_info:
                raise InvalidRequest(WRONG_ID_OR_PW, 400)
            
            user_info = user_info[0]
            
            password_check = bcrypt.checkpw(data["password"].encode("utf-8"), user_info["password"].encode("utf-8"))

            # 데이터베이스의 비밀번호와 일치하지 않으면 에러 처리.
            if password_check is not True:
                raise InvalidRequest(WRONG_ID_OR_PW, 400)
            
            # nickname, password 모두 일치하면 토큰 생성.
            access_token = jwt.encode({"account_id" : user_info["id"]}, SECRET_KEY, algorithm=ALGORITHM)

            return {"message" : "login succeed", "access_token" : access_token}
        
        except Exception as e:
            raise e
