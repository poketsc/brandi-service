from model.product_dao import ProductDao
from model          import CartDao, OrderDao, ShipmentDao, SelectNowDao
from util.exception import *
from util.message   import *

class OrderService:

    def get_order_information(self, connection, filters):

        order_dao    = OrderDao()
        shipment_dao = ShipmentDao()

        # 기본 배송지 정보 가져오기
        shipment_information      = shipment_dao.get_defaulted_true_shipment_information(connection, filters)

        # 배송지 메모 리스트 가져오기
        shipment_memo_information = shipment_dao.get_shipment_memo_information(connection)

        # 주문자 정보 가져오기
        orderer_information       = order_dao.get_orderer_information(connection, filters)  

        result = {
            "shipment_information"      : shipment_information,
            "shipment_memo_information" : shipment_memo_information,
            "orderer_information"       : orderer_information
        }

        return result
    
    def get_order_complete(self, connection, filters):

        order_dao = OrderDao()

        result    = order_dao.get_order_complete_information(connection, filters)

        return result
    
    def post_order(self, connection, filters):

        order_dao    = OrderDao()
        product_dao  = ProductDao()
        now_dao      = SelectNowDao()
        cart_dao     = CartDao()
        shipment_dao = ShipmentDao()
        
        # 외부로 부터 받은 data 복제
        copy_data = filters.copy()

        carts = filters["carts"]

        # 복제 데이터에 carts 삭제
        del copy_data["carts"]
        
        # 현재 시점 선언
        now = now_dao.select_now(connection)
            
        # copy_data 에 현재 시점 추가
        copy_data["now"] = now

        # 주문 추가
        order_id = order_dao.insert_order_information(connection, copy_data)

        # 주문 추가 실패 에러메세지
        if not order_id:
            raise InsertOrderInformationError(INSERT_ORDER_INFORMATION_ERROR, 400)

        copy_data["order_id"] = order_id

        order_history_id = order_dao.insert_order_history_information(connection, copy_data)

        # 주문 히스토리 추가 실패 에러메세지
        if not order_history_id:
            raise InsertOrderHistoryInformationError(INSERT_ORDER_HISTORY_INFORMATION_ERROR, 400)

        # carts의 갯수만큼 for문을 돌려서 각각 데이터 입력
        for cart in carts:
            cart["now"]        = now
            cart["account_id"] = copy_data["account_id"]
            cart["order_id"]   = order_id

            # 상품 존재 여부 확인
            product_id = product_dao.product_exist_check(connection, cart)

            if not product_id:
                raise ProductIdExistError(PRODUCT_ID_DOES_NOT_EXIST, 400)

            # 상품 옵션 sold_out 체크 후 카트에 담기
            product_option_information = product_dao.product_option_sold_out_check(connection, cart)

            # 상품 옵션이 존재하지 않으면 sold_out 에러처리
            if not product_option_information:
                raise ProductOptionSoldOutError(PRODUCT_OPTION_SOLD_OUT, 400)

            # 상품, 상품옵션 아이디 추가
            cart["product_id"]        = product_id["id"]
            cart["product_option_id"] = product_option_information["id"]

            order_product_id   = order_dao.insert_order_product_information(connection, cart)

            if not order_product_id:
                raise InsertOrderProductInformationError(INSERT_ORDER_PRODUCT_INFORMATION_ERROR, 400)
        
            cart["order_product_id"] = order_product_id

            # 카트에 담긴 수량, 할인된 가격 가져오기
            cart_information   = cart_dao.get_cart_information(connection, cart)
            cart["quantity"]   = cart_information[0]["quantity"]

            if cart_information[0]["sale_price"]:
                cart["sale_price"] = cart_information[0]["sale_price"]

            # 주문 상품 히스토리 정보 입력
            order_product_history = order_dao.insert_order_product_history_information(connection, cart)

            if not order_product_history:
                raise InsertOrderProductHistoryInformationError(INSERT_ORDER_PRODUCT_HISTORY_INFORMATION_ERROR, 400)
            
            # copy_data에 order_product_id 담기
            copy_data["order_product_id"] = order_product_id

            # 배송 정보 입력
            shipment_id = shipment_dao.insert_shipment_information(connection, copy_data)

            if not shipment_id:
                raise InsertShipmentInformationError(INSERT_SHIPMENT_INFORMATION_ERROR, 400)
            
            copy_data["shipment_id"] = shipment_id

            # 배송지 정보 가져오기
            shipment_information = shipment_dao.get_one_shipment_information(connection, copy_data)

            copy_data["address"]            = shipment_information["address"]
            copy_data["additional_address"] = shipment_information["additional_address"]
            copy_data["zip_code"]           = shipment_information["zip_code"]
            copy_data["phone_number"]       = shipment_information["phone_number"]
            copy_data["name"]               = shipment_information["name"]

            # 배송지 히스토리 정보 입력
            shipment_dao.insert_shipment_history_information(connection, copy_data)

            # 선분이력을 위한 cart_history_id 가져오기
            cart_history_id         = cart_dao.get_cart_history_id_end_time(connection, cart)
            cart["cart_history_id"] = cart_history_id["cart_history_id"]
            
            # 주문 완료 후 cart_histories에서 시간 끊기
            change_time = cart_dao.update_cart_history_end_time(connection, cart)

            if not change_time:
                raise ChangeTimeError(CHANGE_TIME_ERROR, 400)

            cart["is_deleted"] = True
            # 주문 완료 후 cart_histories에서 cart delete
            change_history_information = cart_dao.update_cart_history_information(connection, cart)

            if not change_history_information:
                raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)
            
            # 상품 옵션 수량 확인
            product_option_stock_check = product_dao.update_product_option_stock(connection, cart)

            if not product_option_stock_check:
                raise ProductOptionStockError(PRODUCT_OPTION_STOCK_ERROR, 400)
            
            # 주문 후 상품 옵션 수량이 -10 이면 sold_out 처리
            product_dao.update_product_option_is_sold_out(connection, cart)

        # 잘 실행 됬으면 order_id 리턴
        data = {"order_id" : order_id}
        return data