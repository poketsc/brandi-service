from model.order_dao import CartDao
from model.util_dao  import SelectNowDao
from util.exception  import ( 
    ProductOptionExistError, ProductOptionSoldOutError,
    CartIdError, ChangeTimeError,
    ChangeHistoryInformationError
)
from util.message    import ( 
    PRODUCT_OPTION_DOES_NOT_EXIST, PRODUCT_OPTION_SOLD_OUT,
    POST_CART_ERROR, CHANGE_TIME_ERROR,
    CHANGE_HISTORY_INFORMATION_ERROR)

class CartService:

    def post_cart(self, data, connection):

        cart_dao = CartDao()
        now_dao = SelectNowDao()

        # sold_out 체크 후 카트에 담기
        product_option_information = cart_dao.product_option_sold_out_check(data, connection)

        # product_option_id 가 존재하지 않으면 에러처리
        if not product_option_information:
            raise ProductOptionExistError(PRODUCT_OPTION_DOES_NOT_EXIST, 400)

        # product_option_id 가 sold_out 이면 에러처리
        if product_option_information['is_sold_out'] == 1:
            raise ProductOptionSoldOutError(PRODUCT_OPTION_SOLD_OUT, 400)
        
        # 카트 정보 확인
        cart_informations = cart_dao.get_cart_information(data, connection)

        # 카트에 같은 상품 존재하는지 확인
        product_duplicate_check = False
        for cart_information in cart_informations:
            if cart_information["product_option_id"] == data["product_option_id"]:
                product_duplicate_check = True
                break
        
        # 현재 시점 선언
        now = now_dao.select_now(connection)

        # data 에 현재 시점 추가
        data['now'] = now

        # 카트에 이미 같은 상품 존재하면 수량 +1
        # 카트 히스토리 선분이력 변경
        if product_duplicate_check:
            # 선분이력 시간 끊기
            change_time = cart_dao.update_cart_history_end_time(data, connection)

            if not change_time:
                raise ChangeTimeError(CHANGE_TIME_ERROR, 400)

            # 선분이력 정보 일괄 변경
            change_history_information = cart_dao.update_cart_history_information(data, connection)

            if not change_history_information:
                raise ChangeHistoryInformationError(CHANGE_HISTORY_INFORMATION_ERROR, 400)

            return change_history_information

        # 카트에 같은 상품이 존재하지 않으면 cart에 상품 담기
        # cart에 상품 담기
        cart_id = cart_dao.post_cart(data, connection)

        if not cart_id:
            raise CartIdError(POST_CART_ERROR, 400)

        # cart에 상품 담은 후 cart_id 받아와서 data에 추가
        data['cart_id'] = cart_id

        # cart 히스토리 생성
        result = cart_dao.post_history_cart(data, connection)

        return result
    
    def get_cart(self, data, connection):

        cart_dao = CartDao()

        results = cart_dao.get_cart_information(data, connection)

        # 할인된가격 (dao에서 가져올수 없어서 service에서 처리해서 results에 추가)

        cart_informations = [{
            "color"             : result["color"],
            "discount_rate"     : result["discount_rate"],
            "korean_name"       : result["korean_name"],
            "name"              : result["name"],
            "price"             : result["price"],
            "quantity"          : result["quantity"],
            "size"              : result["size"],
            "image_url"         : result["image_url"],
            "color_id"          : result["color_id"],
            "size_id"           : result["size_id"],
            "cart_id"           : result["cart_id"],
            "product_option_id" : result["product_option_id"],
            "product_id"        : result["product_id"],
            "discounted_price"  : int((100 - result["discount_rate"]) * result["price"]) * 0.01 if result["discount_rate"] else None
        } for result in results]

        # 총 상품금액, 할인예정 금액, 총 결제 금액 
        total_original_price       = sum([cart_information["price"] for cart_information in cart_informations])
        estimated_discounted_price = sum([cart_information["price"] * cart_information["discount_rate"] if cart_information["discount_rate"] else None for cart_information in cart_informations])
        total_price                = total_original_price - estimated_discounted_price

        # 장바구니(카트)에 필요한 모든 정보 합치기
        cart_information_results = {
            "product_informations"       : cart_informations,
            "total_original_price"       : total_original_price,
            "estimated_discounted_price" : estimated_discounted_price,
            "total_price"                : total_price
        }

        return cart_information_results