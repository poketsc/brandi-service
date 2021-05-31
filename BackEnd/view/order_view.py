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

    @login_required
    @validate_params(
        Param("data", JSON, str, required=True)
    )
    def post(*args):
        cart_service = CartService()
        connection   = None

        filters               = request.json
        filters["account_id"] = g.account_info["account_id"]

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

    @login_required
    def get(self):
        cart_service = CartService()
        connection   = None

        try:
            filters = {
                "account_id" : g.account_info["account_id"]
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
    
    @login_required
    @validate_params(
        Param("cart_id", JSON, int, required=True),
        Param("quantity", JSON, int, required=True)
    )
    def patch(*args):
        cart_service = CartService()
        connection   = None

        filters               = request.json
        filters["account_id"] = g.account_info["account_id"]

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
    
    @login_required
    @validate_params(
        Param("data", JSON, str, required=True)
    )
    def delete(*args):
        cart_service = CartService()
        connection   = None

        filters               = request.json
        filters["account_id"] = g.account_info["account_id"]

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

    @login_required
    def get(self):
        order_service = OrderService()
        connection    = None

        try:
            filters = {
                "account_id" : g.account_info["account_id"]
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
    
    @login_required
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
        filters["account_id"] = g.account_info["account_id"]

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

    @login_required
    @validate_params (
        Param("order_id", PATH, int)
    )
    def get(*args, order_id):
        order_complete_service = OrderCompleteService()
        connection             = None

        filters = {
            "order_id"   : int(order_id),
            "account_id" : g.account_info["account_id"]
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

    @login_required
    @validate_params(
        Param("name", JSON, str, required=True), 
        Param("phone_number", JSON, str, required=True),
        Param("is_defaulted", JSON, bool, required=True),
        Param("address", JSON, str, required=True),
        Param("additional_address", JSON, str, required=True),
        Param("zip_code", JSON, int, required=True),
        Param("is_deleted", JSON, bool, required=True)
    )
    def post(*args):
        shipment_service = ShipmentService()
        connection       = None

        try:
            filters               = request.json
            filters["account_id"] = g.account_info["account_id"]

            connection = connect_db()
            
            result     = shipment_service.insert_address_information(connection, filters)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
                connection.rollback()       
                raise e
        
        finally:
            if connection is not None:
                connection.close()

    @login_required
    @validate_params(
        Param("address_id", JSON, int, required=True),
        Param("name", JSON, str, required=True), 
        Param("phone_number", JSON, str, required=True),
        Param("is_defaulted", JSON, bool, required=True),
        Param("is_deleted", JSON, bool, required=True),
        Param("address", JSON, str, required=True),
        Param("additional_address", JSON, str, required=True),
        Param("zip_code", JSON, int, required=True)
    )
    def patch(*args):
        shipment_service = ShipmentService()
        connection       = None

        try:
            filters               = request.json
            filters["account_id"] = g.account_info["account_id"]

            connection = connect_db()
            
            result     = shipment_service.update_address_information(connection, filters)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
        
        finally:
            if connection is not None:
                connection.close()
    
    @login_required
    def get(self):
        shipment_service = ShipmentService()
        connection       = None

        try:
            filters = {
                "account_id" : g.account_info["account_id"]
            }

            connection = connect_db()

            result     = shipment_service.get_address_information(connection, filters)
            
            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()
    
    @login_required
    @validate_params(
        Param("address_id", JSON, int, required=True)
    )
    def delete(*args):
        shipment_service = ShipmentService()
        connection       = None

        try:
            filters               = request.json
            filters["account_id"] = g.account_info["account_id"]

            connection = connect_db()

            result     = shipment_service.delete_address_information(connection, filters)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()