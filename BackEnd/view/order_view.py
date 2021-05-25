from flask       import request, jsonify
from flask.views import MethodView

from service.order_service   import CartService, OrderService, ShipmentService
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
from util.exception import (
    CartIdTypeError, ProductIdTypeError,
    ProductOptionIdTypeError, PriceTypeError,
    DiscountedPriceTypeError, QuantityTypeError )

from util.message import (
    CART_ID_TYPE_ERROR, PRODUCT_ID_TYPE_ERROR,
    PRODUCT_OPTION_ID_TYPE_ERROR, PRICE_TYPE_ERROR,
    DISCOUNTED_PRICE_TYPE_ERROR, QUANTITY_TYPE_ERROR
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

    # 데코레이터 선언 예정
    def get(self):
        cart_service = CartService()

        connection = None
        try:
            connection = connect_db()

            # user = request.user (데코레이터 사용시 user 선언 방법)

            # 데코레이터가 없어서 user_id를 하드코딩으로 받는방법(테스트용)
            data = {
                'user_id' : 4
            }

            result = cart_service.get_cart(data,connection)

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()
    
    # 데코레이터 선언 예정
    @validate_params(
        Param('user_id', JSON, int, required=True), # 테스트용 user_id
        Param('product_option_id', JSON, int, required=True),
        Param('quantity', JSON, int, required=True),
    )
    def patch(*args):
        cart_service = CartService()

        connection = None
        try:
            connection = connect_db()

            # user = request.user (데코레이터 사용시 user 선언 방법)
            
            data = request.json

            result = cart_service.change_quantity_cart(data, connection)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
            
        finally:
            if connection is not None:
                connection.close()
    
    # 데코레이터 선언 예정
    @validate_params(
        Param('user_id', JSON, int, required=True), # 테스트용 user_id
        Param('product_option_id', JSON, int, required=True)
    )
    def delete(*args):
        cart_service = CartService()

        connection = None
        try:
            connection = connect_db()

            # user = request.user (데코레이터 사용시 user 선언 방법)
            
            data = request.json

            result = cart_service.delete_cart_product(data, connection)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
            
        finally:
            if connection is not None:
                connection.close()

class OrderView(MethodView):

    # 데코레이터 선언 예정
    def get(self):
        order_service = OrderService()

        connection = None
        try:
            connection = connect_db()

            # user = request.user (데코레이터 사용시 user 선언 방법)
            
            data = {
                'user_id' : 4
            }

            result = order_service.get_order_information(data, connection)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
            
        finally:
            if connection is not None:
                connection.close()
    
    # 데코레이터 선언예정
    @validate_params(
        Param('user_id', JSON, int, required=True), # 테스트용 user_id
        Param('cart', JSON, str, required=True), 
        Param('orderer_name', JSON, str, required=True),
        Param('orderer_phone_number', JSON, str, required=True),
        Param('orderer_email', JSON, str, required=True),
        Param('address_id', JSON, int, required=True),
        Param('shipment_memo_id', JSON, int, required=True),
        Param('message', JSON, str, required=False),
        Param('total_price', JSON, int, required=True)
    )
    def post(*args):

        order_service = OrderService()

        connection = None
        try:

            data = request.json

            for i in data['cart']:
                if type(i['cart_id']) != int:
                    raise CartIdTypeError(CART_ID_TYPE_ERROR, 400)
                
                if type(i['product_id']) != int:
                    raise ProductIdTypeError(PRODUCT_ID_TYPE_ERROR, 400)
                
                if type(i['product_option_id']) != int:
                    raise ProductOptionIdTypeError(PRODUCT_OPTION_ID_TYPE_ERROR, 400)
                
                if type(i['price']) != int:
                    raise PriceTypeError(PRICE_TYPE_ERROR, 400)
                
                if type(i['discounted_price']) != int and i["discounted_price"] != None:
                    raise DiscountedPriceTypeError(DISCOUNTED_PRICE_TYPE_ERROR, 400)
                
                if type(i['quantity']) != int:
                    raise QuantityTypeError(QUANTITY_TYPE_ERROR, 400)

            connection = connect_db()

            # data['user_id'] = request.user.id  (데코레이터 사용시 data에 user_id 추가용) 
            
            result = order_service.post_order(data, connection)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            if connection is not None:
                connection.rollback()       
                raise e
        
        finally:
            if connection is not None:
                connection.close()

class ShipmentView(MethodView):

    #데코레이터 선언예정
    @validate_params(
        Param('user_id', JSON, int, required=True), # 테스트용 user_id
        Param('name', JSON, str, required=True), 
        Param('phone_number', JSON, str, required=True),
        Param('is_defaulted', JSON, bool, required=True),
        Param('address', JSON, str, required=True)
    )
    def post(*args):

        shipment_service = ShipmentService()

        connection = None
        try:

            data = request.json

            connection = connect_db()

            # data['user_id'] = request.user.id  (데코레이터 사용시 data에 user_id 추가용)
            
            result = shipment_service.insert_address_information(data, connection)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            if connection is not None:
                connection.rollback()       
                raise e
        
        finally:
            if connection is not None:
                connection.close()