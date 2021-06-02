from model          import CartDao, ProductDao, SelectNowDao
from util.exception import *
from util.message   import *

class CartService:

    def post_cart(self, connection, filters):
        """상품 카트에 담기

        - 상품 품절 여부 확인 후 카트에 담기
        - 카트에 같은 상품이 존재 할때
        - 카트에 같은 상품이 존재하지 않을때

        Author:
            백승찬

        Args:
            filters (dict): 사용자가 수정한 cart_id, quantity 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:
            ProductIdExistError: 존재 하지 않는 상품일때
            ProductOptionSoldOutError: 상품 옵션이 sold_out 일때
            CartIdError: 카트에 상품을 담지 못했을때
            ChangeTimeError: 선분이력 시간 끊기 실패일때
            ChangeHistoryInformationError: 선분이력 정보 추가 실패일때

        Returns:
            200 : 1
        """

        cart_dao    = CartDao()
        product_dao = ProductDao()
        now_dao     = SelectNowDao()

        # account_id 선언
        account_id = {"account_id" : filters["account_id"]}

        # 카트 정보 확인
        cart_informations = cart_dao.get_cart_information(connection, account_id)

        # 현재 시점 선언
        now               = now_dao.select_now(connection)

        for filter in filters["data"]:

            # 상품 존재 여부 확인
            product_id = product_dao.product_exist_check(connection, filter)

            if not product_id:
                raise ProductIdExistError(PRODUCT_ID_DOES_NOT_EXIST, 400)

            # 상품 옵션 sold_out 체크 후 카트에 담기
            product_option_information = product_dao.product_option_sold_out_check(connection, filter)

            # 상품 옵션이 존재하지 않으면 sold_out 에러처리
            if not product_option_information:
                raise ProductOptionSoldOutError(PRODUCT_OPTION_SOLD_OUT, 400)
            
            # 카트에 같은 상품 존재하는지 확인
            product_duplicate_check = False
            for cart_information in cart_informations:
                if cart_information["product_option_id"] == filter["product_option_id"]:
                    product_duplicate_check = True
                    break
            
            filter["now"]        = now
            filter["account_id"] = filters["account_id"]

            # 카트에 같은 상품이 존재하지 않으면 cart에 상품 담기
            if not product_duplicate_check:
                cart_id = cart_dao.post_cart(connection, filter)

                if not cart_id:
                    raise CartIdError(POST_CART_ERROR, 400)

                # cart에 상품 담은 후 cart_id 받아와서 data에 추가
                filter["cart_id"] = cart_id

                # cart 히스토리 생성
                cart_dao.post_history_cart(connection, filter)

            # 카트에 이미 같은 상품 존재하면 수량 +1
            # 카트 히스토리 선분이력 변경
            else:
                # filters에 해당 카트 아이디 추가
                filter["cart_id"] = cart_information["cart_id"]

                # 선분이력을 위한 cart_history_id 가져오기
                cart_history_id           = cart_dao.get_cart_history_id_end_time(connection, filter)
                filter["cart_history_id"] = cart_history_id["cart_history_id"]

                # 선분이력 시간 끊기
                change_time = cart_dao.update_cart_history_end_time(connection, filter)

                if not change_time:
                    raise ChangeTimeError(CHANGE_TIME_ERROR, 400)

                # 선분이력 정보 일괄 변경
                change_history_information = cart_dao.update_cart_history_information(connection, filter)

                if not change_history_information:
                    raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)

        return 1

    def get_cart(self, connection, filters):
        """카트 정보 가져오기

        Author:
            백승찬

        Args:
            filters (dict): 사용자의 아이디 값을 가지는 dictionary
            connection (객체): pymysql 객체
        
        Raises:

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

        cart_dao          = CartDao()
        cart_informations = cart_dao.get_cart_information(connection, filters)

        return cart_informations
    
    def change_quantity_cart(self, connection, filters):
        """카트에 담긴 제품 수량 변경

        Author:
            백승찬

        Args:
            filters (dict): 사용자의 아이디, cart_id, quantity 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:
            ProductIdExistError: 상품이 존재하지 않을때
            ProductOptionSoldOutError: 상품 옵션이 sold_out 일때
            ChangeTimeError: 선분이력 시간 끊기 실패
            ChangeHistoryInformationError: 선분이력 정보 추가 실패

        Returns:
            200 : 1
        """

        cart_dao    = CartDao()
        product_dao = ProductDao()
        now_dao     = SelectNowDao()

        # 상품 존재 여부 확인
        product_id = product_dao.product_exist_check(connection, filters)

        if not product_id:
            raise ProductIdExistError(PRODUCT_ID_DOES_NOT_EXIST, 400)

        # 상품 옵션 sold_out 체크 후 카트에 담기
        product_option_information = product_dao.product_option_sold_out_check(connection, filters)

        # 상품 옵션이 존재하지 않으면 sold_out 에러처리
        if not product_option_information:
            raise ProductOptionSoldOutError(PRODUCT_OPTION_SOLD_OUT, 400)

        # 현재 시점 선언
        now            = now_dao.select_now(connection)
        filters["now"] = now

        # 선분이력을 위한 cart_history_id 가져오기
        cart_history_id            = cart_dao.get_cart_history_id_end_time(connection, filters)
        filters["cart_history_id"] = cart_history_id["cart_history_id"]

        # 선분이력 시간 끊기
        change_time = cart_dao.update_cart_history_end_time(connection, filters)

        if not change_time:
            raise ChangeTimeError(CHANGE_TIME_ERROR, 400)
        
        # 선분이력 복사, 원하는 형태로 데이터 수정
        change_history_information = cart_dao.update_cart_history_information(connection, filters)

        if not change_history_information:
            raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)
        
        return change_history_information
    
    def delete_cart_product(self, connection, filters):
        """카트에 담긴 상품들 삭제

        Author:
            백승찬

        Args:
            filters (dict): 사용자의 아이디, 다수의 cart_id 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:
            ChangeTimeError: 선분이력 시간 끊기 실패할때
            ChangeHistoryInformationError: 선분이력 정보 추가 실패할때

        Returns:
            200 : 1
        """

        cart_dao = CartDao()
        now_dao  = SelectNowDao()

        # 현재 시점 선언
        now = now_dao.select_now(connection)

        for filter in filters["data"]:

            filter["now"]        = now
            filter["account_id"] = filters["account_id"]

            # 선분이력을 위한 cart_history_id 가져오기
            cart_history_id           = cart_dao.get_cart_history_id_end_time(connection, filter)
            filter["cart_history_id"] = cart_history_id["cart_history_id"]

            # 선분이력 시간 끊기
            change_time = cart_dao.update_cart_history_end_time(connection, filter)

            if not change_time:
                raise ChangeTimeError(CHANGE_TIME_ERROR, 400)
            
            # 선분이력 복사, 원하는 형태로 데이터 수정
            filter["is_deleted"]       = True
            change_history_information = cart_dao.update_cart_history_information(connection, filter)

            if not change_history_information:
                raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)
            
        return change_history_information