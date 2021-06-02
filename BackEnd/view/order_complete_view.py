from flask       import jsonify, g
from flask.views import MethodView

from util.decorator          import login_required
from service                 import OrderService
from connection              import connect_db
from flask_request_validator import *

from util.exception import *
from util.message   import *

class OrderCompleteView(MethodView):

    @login_required
    @validate_params (
        Param("order_id", PATH, int)
    )
    def get(*args, order_id):
        """결제 완료 페이지 정보 가져오기

        Author:
            백승찬

        Args:
            (PATH): order_id를 path parameter로 받음 

        Raises:
            OrderIdTypeError: order_id 가 int 타입이 아닐때
            e: 예상하지 못한 에러처리

        Returns:
            200 : {
                "data": {
                    "id": 주문번호
                    "total_price": 총 결제 금액
                    }
                }
        """

        order_service = OrderService()
        connection    = None

        filters = {
            "order_id"   : int(order_id),
            "account_id" : g.account_info["account_id"]
        }

        if type(filters["order_id"]) != int:
            raise OrderIdTypeError(ORDER_ID_TYPE_ERROR, 400)

        try:
            connection = connect_db()

            result     = order_service.get_order_complete(connection, filters)
            
            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()