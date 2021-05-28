from flask       import request, jsonify, g
from flask.views import MethodView

from util.decorator          import login_required
from service                 import CartService, OrderService, ShipmentService, OrderCompleteService
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
from util.exception import *
from util.message   import *

class CartView(MethodView):

    # @login_required
    @validate_params(
        Param("data", JSON, str, required=True)
    )
    def post(*args):
        cart_service = CartService()
        connection   = None

        filters               = request.json
        # filters["account_id"] = g.account_info["account_id"]
        filters["account_id"] = 4

        for filter in filters["data"]:
            if type(filter["product_option_id"]) != int:
                raise ProductOptionIdTypeError(PRODUCT_OPTION_ID_TYPE_ERROR, 400)
            
            if type(filter["quantity"]) != int:
                raise QuantityTypeError(QUANTITY_TYPE_ERROR, 400)
            
            if filter["quantity"] <= 0:
                raise CartQuantityError(CART_QUANTITY_ERROR, 400)

        try:
            connection = connect_db()

            result = cart_service.post_cart(connection, filters)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
                connection.rollback()
                raise e

        finally:
            if connection is not None:
                connection.close()

    # @login_required
    def get(self):
        cart_service = CartService()
        connection   = None

        try:
            filters = {
                # "account_id" : g.account_info["account_id"]
                "account_id" : 4
            }

            connection = connect_db()

            result     = cart_service.get_cart(connection, filters)

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()
    
    # @login_required
    @validate_params(
        Param("cart_id", JSON, int, required=True),
        Param("quantity", JSON, int, required=True)
    )
    def patch(*args):
        cart_service = CartService()
        connection   = None

        filters               = request.json
        # filters["account_id"] = g.account_info["account_id"]
        filters["account_id"] = 4

        if filters["quantity"] <= 0:
            raise CartQuantityError(CART_QUANTITY_ERROR, 400)

        try:
            connection = connect_db()

            result     = cart_service.change_quantity_cart(connection, filters)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
            
        finally:
            if connection is not None:
                connection.close()
    
    # @login_required
    @validate_params(
        Param("data", JSON, str, required=True)
    )
    def delete(*args):
        cart_service = CartService()
        connection   = None

        filters               = request.json
        # filters["account_id"] = g.account_info["account_id"]
        filters["account_id"] = 4

        for filter in filters["data"]:
            if type(filter["cart_id"]) != int:
                raise CartIdTypeError(CART_ID_TYPE_ERROR, 400)

        try:
            connection = connect_db()

            result     = cart_service.delete_cart_product(connection, filters)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
            
        finally:
            if connection is not None:
                connection.close()

class OrderView(MethodView):

    # @login_required
    def get(self):
        order_service = OrderService()
        connection    = None

        try:
            filters = {
                # "account_id" : g.account_info["account_id"]
                "account_id" : 4
            }

            connection = connect_db()

            result     = order_service.get_order_information(connection, filters)

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
            
        finally:
            if connection is not None:
                connection.close()
    
    # @login_required
    @validate_params(
        Param("carts", JSON, str, required=True), 
        Param("orderer_name", JSON, str, required=True),
        Param("orderer_phone_number", JSON, str, required=True),
        Param("orderer_email", JSON, str, required=True),
        Param("address_id", JSON, int, required=True),
        Param("shipment_memo_id", JSON, int, required=True),
        Param("message", JSON, str, required=False),
        Param("total_price", JSON, int, required=True)
    )
    def post(*args):
        order_service = OrderService()
        connection    = None

        filters               = request.json
        # filters["account_id"] = g.account_info["account_id"]
        filters["account_id"] = 4

        for filter in filters["carts"]:
            if type(filter['cart_id']) != int:
                raise CartIdTypeError(CART_ID_TYPE_ERROR, 400)

        try:
            connection = connect_db()
            
            result     = order_service.post_order(connection, filters)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
        
        finally:
            if connection is not None:
                connection.close()
    
class OrderCompleteView(MethodView):

    # @login_required
    @validate_params (
        Param("order_id", PATH, int)
    )
    def get(*args, order_id):
        order_complete_service = OrderCompleteService()
        connection             = None

        filters = {
            "order_id"   : int(order_id),
            "account_id" : 4
            # "account_id" : g.account_info["account_id"]
        }

        if type(filters["order_id"]) != int:
            raise OrderIdTypeError(ORDER_ID_TYPE_ERROR, 400)

        try:
            connection = connect_db()

            result     = order_complete_service.get_order_complete(connection, filters)
            
            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
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

    #데코레이터 선언예정
    @validate_params(
        Param('user_id', JSON, int, required=True), # 테스트용 user_id
        Param('id', JSON, int, required=True),
        Param('address_id', JSON, int, required=True),
        Param('name', JSON, str, required=True), 
        Param('phone_number', JSON, str, required=True),
        Param('is_defaulted', JSON, bool, required=True),
        Param('address', JSON, str, required=True)
    )
    def patch(*args):

        shipment_service = ShipmentService()

        connection = None
        try:

            data = request.json

            connection = connect_db()

            # data['user_id'] = request.user.id  (데코레이터 사용시 data에 user_id 추가용)
            
            result = shipment_service.update_address_information(data, connection)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            if connection is not None:
                connection.rollback()       
                raise e
        
        finally:
            if connection is not None:
                connection.close()
    
    # 데코레이터 선언 예정
    def get(self):
        shipment_service = ShipmentService()

        connection = None
        try:
            connection = connect_db()

            # user = request.user (데코레이터 사용시 user 선언 방법)

            # 데코레이터가 없어서 user_id를 하드코딩으로 받는방법(테스트용)
            data = {
                'user_id' : 4
            }

            result = shipment_service.get_address_information(data, connection)
            
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
        Param('id', JSON, int, required=True),
        Param('address_id', JSON, int, required=True),
        Param('name', JSON, str, required=True), 
        Param('phone_number', JSON, str, required=True),
        Param('is_defaulted', JSON, bool, required=True),
        Param('address', JSON, str, required=True)
    )
    def delete(*args):
        shipment_service = ShipmentService()

        connection = None
        try:
            
            data = request.json

            connection = connect_db()

            # user = request.user (데코레이터 사용시 user 선언 방법)

            result = shipment_service.delete_address_information(data, connection)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()