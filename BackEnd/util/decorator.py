import jwt

from functools        import wraps
from flask            import request, g

from model            import AccountDao
from util.exception   import InvalidAccessError, LoginRequiredError
from util.message     import UNAUTHORIZED_TOKEN, LOGIN_REQUIRED
from util.const       import USER_ACCOUNT_TYPE
from config           import SECRET_KEY, ALGORITHM
from connection       import connect_db

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        
        if access_token is None:
            raise LoginRequiredError(LOGIN_REQUIRED, 401)
            
        connection = None
        
        try:
            # 헤더에 있는 토큰을 디코드해서 payload에 담는다.
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)

            # payload = {"account_id"    : user_info["account_id"]}

            account_dao = AccountDao()
            connection  = connect_db()

            account = account_dao.account_check(connection, payload)

            if account["account_type_id"] != USER_ACCOUNT_TYPE:
                raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            if account["is_deleted"] == 1:
                raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            g.account_info = {"account_id" : payload["account_id"]}

        except jwt.InvalidTokenError:
            raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()
        
        return func(*args, **kwargs)
    return wrapper
