from flask       import request, jsonify, g
from flask.views import MethodView

from util.decorator          import login_required
from service                 import OrderService
from connection              import connect_db
from flask_request_validator import *

from util.exception import *
from util.message   import *

class OrderView(MethodView):

    @login_required
    def get(self):
        """주문하기 페이지 정보 가져오기

        Author:
            백승찬

        Args:

        Raises:
            e: 예상하지 못한 에러처리

        Returns:
            {
            "data": {
                        "orderer_information": {
                            "orderer_email"        : 주문자 이메일
                            "orderer_name"         : 주문자 이름
                            "orderer_phone_number" : 주문자 전화번호
                        },
                        "shipment_information": {
                            "additional_address" : 추가 주소 정보
                            "address"            : 주소
                            "address_history_id" : 주소 히스토리 아이디
                            "address_id"         : 주소 아이디
                            "is_deleted"         : 삭제 여부
                            "name"               : 수령인
                            "phone_number"       : 수령인 전화번호
                            "zip_code"           : 우편번호
                        },
                        "shipment_memo_information": [
                            {
                                "content": 배송메모
                                "id": 1
                            },
                            {
                                "content": 배송메모
                                "id": 2
                            },
                            {
                                "content": 배송메모
                                "id": 3
                            },
                            {
                                "content": 배송메모
                                "id": 4
                            }
                        ]
                    }
            }
        """
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
        Param("orderer_name", JSON, str, required=True),
        Param("orderer_phone_number", JSON, str, required=True),
        Param("orderer_email", JSON, str, required=True),
        Param("address_id", JSON, int, required=True),
        Param("shipment_memo_id", JSON, int, required=True),
        Param("message", JSON, str, required=False),
        Param("total_price", JSON, int, required=True)
    )
    def post(self, valid: ValidRequest):
        """주문하기 기능

        Author:
            백승찬

        Args:
            {
                "orderer_name"         : 주문자 이름
                "orderer_phone_number" : 주문자 번호
                "orderer_email         : 주문자 이메일
                "address_id"           : 주소 아이디
                "shipment_memo_id"     : 배송 메모 아이디
                "message"              : 직접입력 시 입력하는 message
                "total_price"          : 결제 총액
            }

        Raises:
            CartIdTypeError: 리스트로 들어온 다수의 cart_id가 int 타입이 아니면 에러처리
            e: 예상하지 못한 에러처리

        Returns:
            { "data": {
                "order_id": 주문번호
                }
            }
        """
        order_service = OrderService()
        connection    = None

        filters               = valid.get_json()
        filters["account_id"] = g.account_info["account_id"]
        filters["carts"]      = request.json["carts"]

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