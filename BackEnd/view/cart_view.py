from flask       import request, jsonify, g
from flask.views import MethodView

from util.decorator          import login_required
from service                 import CartService
from connection              import connect_db
from flask_request_validator import *

from util.exception import *
from util.message   import *

class CartView(MethodView):

    @login_required
    def post(self):
        """장바구니 담기
        
        - 한번에 여러개의 상품 담기 가능
        - 이미 같은 상품 옵션이 담겨 있으면 수량 변화

        Author:
            백승찬

        Args:
            data (dict): 사용자가 추가한 product_option_id, quantity 값을 가지는 dictionary

        Raises:
            ProductOptionIdTypeError: product_option_id 타입이 int 가 아닐때
            QuantityTypeError: quantity 타입이 int가 아닐때
            CartQuantityError: 수량이 1개 미만일때
            e: 예상하지 못한 에러처리
        

        Returns:
            200: {   
                "data": 1
                }
        """

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
        """장바구니 정보 가져오기
        
        - 장바구니에 담긴 모든 상품 정보 가져오기
        - 상품 품절 여부 체크 후 정보 가져오기

        Author:
            백승찬
        
        Args:


        Raises:
            e: 예상하지 못한 에러처리

        Returns:
            {
                "data": [
            {
                "cart_id": cart_id 정보
                "color": 상품 색상
                "color_id": 색상 아이디
                "discount_rate": 할인률
                "estimated_discount_price": 할인 예상 금액
                "image_url": 대표 이미지 url
                "korean_name": 셀러 이름
                "name": 제품 이름
                "price": 제품 가격
                "product_id": 상품 아이디
                "product_option_id": 상품 옵션 아이디
                "quantity": 수량
                "sale_price": 할인된 금액
                "seller_id": 셀러 아이디
                "size": 크기
                "size_id": 사이즈 아이디
            }
        ]
    }
        """

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
    def patch(self, valid: ValidRequest):
        """카트 수량 변경

        - 카트에 담긴 제품 수량 변경시 이력관리
        - 수량 변경시 1개 미만으로 선택시 에러처리

        Author:
            백승찬
        
        Args:
            cart_id (dict): 사용자가 수정한 cart_id 값을 가지는 dictionary
            quantity (dict): 사용자가 수정한 quantity 값을 가지는 dictionary

        Raises:
            CartQuantityError: 수량 선택이 1개 미만일때 에러처리
            e: 예상하지 못한 에러처리

        Returns:
            200 : {
                    "data": 1
                }
        """

        cart_service = CartService()
        connection   = None

        filters               = valid.get_json()
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
    def delete(self):
        """카트 상품 삭제

        - 한번에 여러 상품 삭제 가능

        Author:
            백승찬

        Args:
            data (dict): 사용자가 삭제한 cart_id 리스트

        Raises:
            CartIdTypeError: cart_id 가 int 타입이 아닐때
            e: 예상하지 못한 에러처리

        Returns:
            200 : {
                "data": 1
            }

        """
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