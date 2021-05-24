from flask       import request, jsonify
from flask.views import MethodView

from service.order_service   import CartService
from connection              import connect_db
from flask_request_validator import (
    GET,
    FORM,
    PATH,
    JSON,
    Param,
    Pattern,
    MinLength,
    MaxLength,
    validate_params
)

class CartView(MethodView):

    #데코레이터 선언 예정
    @validate_params(
        Param('user_id', JSON, int, required=True), # 테스트용 user_id
        Param('product_option_id', JSON, int, required=True),
        Param('quantity', JSON, int, required=True),
    )
    def post(*args):
        cart_service = CartService()

        connection = None
        try:
            connection = connect_db()
            
            data = request.json

            # data['user_id'] = request.user.id  (데코레이터 사용시 data에 user_id 추가용) 
            
            result = cart_service.post_cart(data, connection)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
        
        finally:
            if connection is not None:
                connection.close()