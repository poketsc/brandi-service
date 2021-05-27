from model          import CartDao, OrderDao, ShipmentDao, SelectNowDao
from util.exception import *
from util.message   import *

class CartService:

    def post_cart(self, connection, filters):

        cart_dao = CartDao()
        now_dao  = SelectNowDao()
        
        # sold_out 체크 후 카트에 담기
        product_option_information = cart_dao.product_option_sold_out_check(connection, filters)

        # 상품이 존재하지 않으면 에러처리
        if not product_option_information:
            raise ProductOptionExistError(PRODUCT_OPTION_DOES_NOT_EXIST, 400)

        # 상품 옵션이 sold_out 이면 에러처리
        if product_option_information["is_sold_out"] == 1:
            raise ProductOptionSoldOutError(PRODUCT_OPTION_SOLD_OUT, 400)
        
        # 카트 정보 확인
        cart_informations = cart_dao.get_cart_information(connection, filters)

        # 카트에 같은 상품 존재하는지 확인
        product_duplicate_check = False
        for cart_information in cart_informations:
            if cart_information["product_option_id"] == filters["product_option_id"]:
                product_duplicate_check = True
                break
        
        # 현재 시점 선언
        now            = now_dao.select_now(connection)
        filters["now"] = now

        # 카트에 이미 같은 상품 존재하면 수량 +1
        # 카트 히스토리 선분이력 변경
        if product_duplicate_check:
            # 선분이력 시간 끊기
            change_time = cart_dao.update_cart_history_end_time(connection, filters)

            if not change_time:
                raise ChangeTimeError(CHANGE_TIME_ERROR, 400)

            # 선분이력 정보 일괄 변경
            change_history_information = cart_dao.update_cart_history_information(connection, filters)

            if not change_history_information:
                raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)

            return change_history_information

        # 카트에 같은 상품이 존재하지 않으면 cart에 상품 담기
        cart_id = cart_dao.post_cart(connection, filters)

        if not cart_id:
            raise CartIdError(POST_CART_ERROR, 400)

        # cart에 상품 담은 후 cart_id 받아와서 data에 추가
        filters['cart_id'] = cart_id

        # cart 히스토리 생성
        result = cart_dao.post_history_cart(connection, filters)

        return result
    
    def get_cart(self, connection, filters):

        cart_dao          = CartDao()
        cart_informations = cart_dao.get_cart_information(connection, filters)

        # 총 상품금액, 할인예정 금액, 총 결제 금액 
        total_original_price       = sum([cart_information["price"] for cart_information in cart_informations])
        estimated_discounted_price = sum([cart_information["estimated_discount_price"] for cart_information in cart_informations])
        total_payment              = total_original_price - estimated_discounted_price

        # 장바구니(카트)에 필요한 모든 정보 합치기
        cart_information_results = {
            "product_informations"       : cart_informations,
            "total_original_price"       : total_original_price,
            "estimated_discounted_price" : estimated_discounted_price,
            "total_payment"              : total_payment
        }

        return cart_information_results
    
    def change_quantity_cart(self, connection, filters):

        cart_dao = CartDao()
        now_dao  = SelectNowDao()

        # sold_out 체크 후 카트에 담기
        product_option_information = cart_dao.product_option_sold_out_check(connection, filters)

        # 상품이 존재하지 않으면 에러처리
        if not product_option_information:
            raise ProductOptionExistError(PRODUCT_OPTION_DOES_NOT_EXIST, 400)

        # 상품 옵션이 sold_out 이면 에러처리
        if product_option_information["is_sold_out"] == 1:
            raise ProductOptionSoldOutError(PRODUCT_OPTION_SOLD_OUT, 400)

        # 현재 시점 선언
        now            = now_dao.select_now(connection)
        filters['now'] = now

        # 선분이력 시간 끊기
        change_time = cart_dao.update_cart_history_end_time(connection, filters)

        if not change_time:
            raise ChangeTimeError(CHANGE_TIME_ERROR, 400)
        
        # 선분이력 복사, 원하는 형태로 데이터 수정
        change_history_information = cart_dao.update_cart_history_information(connection, filters)

        if not change_history_information:
            raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)
        
        return change_history_information
    
    def delete_cart_product(self, data, connection):

        cart_dao = CartDao()
        now_dao = SelectNowDao()

        # 현재 시점 선언
        now = now_dao.select_now(connection)
            
        # data 에 현재 시점 추가
        data['now'] = now

        # 선분이력 시간 끊기
        change_time = cart_dao.update_cart_history_end_time(data, connection)

        if not change_time:
            raise ChangeTimeError(CHANGE_TIME_ERROR, 400)
        
        return change_time
    
class OrderService:

    def get_order_information(self, data, connection):

        order_dao = OrderDao()

        # 기본 배송지 정보 가져오기
        shipment_information = order_dao.get_defaulted_true_shipment_information(data, connection)

        # 배송지 메모 리스트 가져오기
        shipment_memo_information = order_dao.get_shipment_memo_information(connection)

        result = {
            "shipment_information" : shipment_information,
            "shipment_memo_information" : shipment_memo_information
        }

        return result
    
    def post_order(self, data, connection):

        order_dao = OrderDao()
        now_dao   = SelectNowDao()
        cart_dao  = CartDao()
        
        # 외부로 부터 받은 data 복제
        copy_data = data.copy()

        carts = {
            "cart" : data["cart"]
        }

        # cart 삭제
        del copy_data["cart"]
        
        # 현재 시점 선언
        now = now_dao.select_now(connection)
            
        # copy_data 에 현재 시점 추가
        copy_data['now'] = now

        # 주문 추가
        order_id = order_dao.insert_order_information(copy_data, connection)

        # 주문 추가 실패 에러메세지
        if not order_id:
            raise InsertOrderInformationError(INSERT_ORDER_INFORMATION_ERROR, 400)

        copy_data['order_id'] = order_id

        order_history_id = order_dao.insert_order_history_information(copy_data, connection)

        # 주문 히스토리 추가 실패 에러메세지
        if not order_history_id:
            raise InsertOrderHistoryInformationError(INSERT_ORDER_HISTORY_INFORMATION_ERROR, 400)

        # cart의 갯수만큼 for문을 돌려서 각각 데이터 입력
        for cart in carts['cart']:
            cart['now'] = now
            cart['user_id'] = data['user_id']
            cart['order_id'] = order_id           
            order_product_id = order_dao.insert_order_product_information(cart, connection)

            if not order_product_id:
                raise InsertOrderProductInformationError(INSERT_ORDER_PRODUCT_INFORMATION_ERROR, 400)
        
            cart['order_product_id'] = order_product_id

            # 주문 상품 히스토리 정보 입력
            order_product_history = order_dao.insert_order_product_history_information(cart, connection)

            if not order_product_history:
                raise InsertOrderProductHistoryInformationError(INSERT_ORDER_PRODUCT_HISTORY_INFORMATION_ERROR, 400)
            
            # copy_data에 order_product_id 담기
            copy_data['order_product_id'] = order_product_id

            # 배송 정보 입력
            result = order_dao.insert_shipment_information(copy_data, connection)

            if not result:
                raise InsertShipmentInformationError(INSERT_SHIPMENT_INFORMATION_ERROR, 400)
            
            # 주문 완료 후 cart_histories에서 cart delete
            change_time = cart_dao.update_cart_history_end_time(cart, connection)

            if not change_time:
                raise ChangeTimeError(CHANGE_TIME_ERROR, 400)

        # 잘 실행 됬으면 1 리턴
        return change_time

class ShipmentService:
    
    def insert_address_information(self, data, connection):

        shipment_dao = ShipmentDao()
        order_dao    = OrderDao()
        now_dao      = SelectNowDao()

        # 현재 시점 선언
        now = now_dao.select_now(connection)
            
        # data 에 현재 시점 추가
        data['now'] = now

        shipment_information = shipment_dao.get_all_shipment_information(data, connection)

        # 배송지 주소 정보가 5개 일때
        if len(shipment_information) == 5:
            raise MaximumShipmentInformationError(MAXIMUM_SHIPMENT_INFORMATION_ERROR, 400)

        # 기본 배송지로 설정할때
        if data['is_defaulted'] == True:
            address_id = shipment_dao.insert_address_information(data, connection)

            data['address_id'] = address_id

            defaulted_true = order_dao.get_defaulted_true_shipment_information(data, connection)

            # 기존에 기본 배송지가 존재하지 않는 경우
            if not defaulted_true:
                insert_address_history = shipment_dao.insert_address_history_information(data, connection)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)

                return insert_address_history
            
            # 기존에 기본 배송지가 존재하는 경우
            defaulted_true['now'] = now
            update_address = shipment_dao.update_address_history_end_time(defaulted_true, connection)

            if not update_address:
                raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)
            
            defaulted_true['is_defaulted'] = False
            insert_address_history = shipment_dao.insert_address_history_information(defaulted_true, connection)

            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            data['address_id'] = address_id
            insert_address_history = shipment_dao.insert_address_history_information(data, connection)

            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            return insert_address_history
        
        # 기본 배송지로 설정하지 않을때
        address_id = shipment_dao.insert_address_information(data, connection)

        data['address_id'] = address_id

        # 이전에 주소를 설정한적이 없으면 기본 배송지로 자동 설정
        if len(shipment_information) == 0:
            data['is_defaulted'] = True
            insert_address_history = shipment_dao.insert_address_history_information(data, connection)

            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)

            return insert_address_history
        
        insert_address_history = shipment_dao.insert_address_history_information(data, connection)

        return insert_address_history
    
    # 이미 등록된 배송지 정보 바꿀때
    def update_address_information(self, data, connection):

        shipment_dao = ShipmentDao()
        now_dao      = SelectNowDao()
        order_dao    = OrderDao()

        # 현재 시점 선언
        now = now_dao.select_now(connection)
            
        # data 에 현재 시점 추가
        data['now'] = now

        # 기본 배송지 가져오기
        defaulted_true = order_dao.get_defaulted_true_shipment_information(data, connection)
        
        # 기본 배송지 정보 수정할때
        if data['id'] == defaulted_true['id']:
            # 데이터 정보 insert
            insert_address_history = shipment_dao.insert_address_history_information(data, connection)

            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)

            # insert 후 이전 기본 배송지 시간 끊기
            data['is_defaulted'] = False
            update_address=shipment_dao.update_address_history_end_time(data, connection)
            
            if not update_address:
                raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)
            
            return update_address

        # 일반 배송지를 기본 배송지로 선택할 때
        if data['is_defaulted'] == True:
            
            # 기본 배송지에 정보 추가,수정
            defaulted_true['now'] = now

            # 기본 배송지 end_time 변경
            update_address_end_time = shipment_dao.update_address_history_end_time(defaulted_true, connection)
            if not update_address_end_time:
                raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)
            
            defaulted_true['is_defaulted'] = False
            insert_address_history = shipment_dao.insert_address_history_information(defaulted_true, connection)

            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            # 변경할 데이터 시간 끊기
            data['is_defaulted'] = False
            update_address_end_time = shipment_dao.update_address_history_end_time(data, connection)

            if not update_address_end_time:
                raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

            # 변경할 데이터 정보 insert
            data['is_defaulted'] = True
            insert_address_history = shipment_dao.insert_address_history_information(data, connection)

            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            return insert_address_history

        # 일반 배송지 일반 정보만 수정할 때
        # 변경할 데이터 시간 끊기
        update_address_end_time = shipment_dao.update_address_history_end_time(data, connection)
        if not update_address_end_time:
            raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

        # 변경할 데이터 정보 insert
        insert_address_history = shipment_dao.insert_address_history_information(data, connection)
        if not insert_address_history:
            raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
        return insert_address_history

    def get_address_information(self, data, connection):

        shipment_dao = ShipmentDao()

        # 배송지 정보 가져오기
        shipment_information = shipment_dao.get_all_shipment_information(data, connection)

        return shipment_information
    
    def delete_address_information(self, data, connection):

        shipment_dao = ShipmentDao()
        now_dao      = SelectNowDao()

        # 현재 시점 선언
        now = now_dao.select_now(connection)
            
        # data 에 현재 시점 추가
        data['now'] = now


        if data['is_defaulted'] == True:
            raise DeleteAddressInformationError(DELETE_ADDRESS_INFORMATION_ERROR, 400)

        # 데이터 정보 시간 끊기
        data['is_deleted'] = False
        update_address_end_time = shipment_dao.update_address_history_end_time(data, connection)
        if not update_address_end_time:
            raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

        # 변경할 데이터 정보 insert
        data['is_deleted'] = True
        insert_address_history = shipment_dao.insert_address_history_information(data, connection)
        if not insert_address_history:
            raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
        
        return insert_address_history