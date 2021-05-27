from flask                   import request, jsonify
from flask.views             import MethodView
from flask_request_validator import validate_params, Param, JSON

from service              import SignInService
from connection           import connect_db

class AccountView(MethodView):
    
    @validate_params(
    Param("nickname", JSON, str, required=True),
    Param("password", JSON, str, required=True)
    )
    def post(*args):
        """
        클라이언트로부터 nickname과 password를 받는다.
        nickname으로 데이터베이스에서 유저 정보 가져오기.
        아이디가 존재하는지 확인하고 에러 처리.
        데이터베이스 비밀번호와 일치하지 않으면 에러 처리.
        둘 다 일치하면 토큰 발급해서 리턴.
        """
        sign_in_service = SignInService()
        
        connection = None

        try:
            data       = request.json
            connection = connect_db()

            # nickname으로 데이터베이스에서 user 정보 가져오기.
            result = sign_in_service.post_sign_in(connection, data)
            
            return jsonify(result), 200
        
        except Exception as e:
            if connection is not None:
                connection.rollback()
            raise e
        
        finally:
            if connection is not None:
                connection.close()