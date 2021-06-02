from flask                   import jsonify, request
from flask.views             import MethodView
from flask_request_validator import *

from service    import ProductService
from connection import connect_db

class ProductDetailView(MethodView):

    @validate_params (
        Param("product_id", PATH, int),
        Param("offset", GET, int, required=False),
        Param("limit", GET, int, required=False)
    )
    def get(*args, product_id):
        """제품 상세 정보 가져오기

        Author:
            백승찬

        Args:
            product_id (PATH) : 제품 번호
            offset (GET)      : 몇번째 로우부터 시작할지
            limit  (GET)      : 출력할 행의 수

        Raises:
            e: 예상하지 못한 에러

        Returns:
            {  "data": {
                            "product_detail": {
                                "detail_page_html"     : 상품 정보
                                "discount_rate"        : 할인률
                                "korean_name"          : 셀러 이름
                                "name"                 : 제품 이름
                                "price"                : 제품 가격
                                "sale_price"           : 제품 할인된 가격
                                "seller_id"            : 셀러 아이디
                                "shipment_information" : 배송 정보
                                "total_order"          : 구매중(총 주문개수)
                            },
                            "product_image": [
                                {
                                    "image_url" : 제품 이미지
                                    "is_main"   : 대표 이미지 여부
                                },
                                {
                                    "image_url" : 제품 이미지
                                    "is_main"   : 대표 이미지 여부
                                }
                            ],
                            "product_option_information": [
                                {
                                    "color" : 색상
                                    "id"    : 제품 옵션 아이디
                                    "size"  : 크기
                                },
                                {
                                    "color" : 색상
                                    "id"    : 제품 옵션 아이디
                                    "size"  : 크기
                                },
                                {
                                    "color" : 색상 
                                    "id"    : 제품 옵션 아이디
                                    "size"  : 크기
                                }
                            ],
                            "related_product_list": [
                                {
                                    "discount_rate" : 할인률
                                    "id"            : 제품 아이디
                                    "image"         : 제품 대표 이미지
                                    "name"          : 제품 이름
                                    "price"         : 제품 가격
                                    "sale_price"    : 제품 할인된 가격
                                    "seller_id"     : 셀러 아이디
                                    "seller_name"   : 셀러 이름
                                }
                            ]
                        }
                    }
        """

        filters = {
            "offset"     : int(request.args.get("offset", 0)),
            "limit"      : int(request.args.get("limit", 5)),
            "product_id" : int(product_id)
        }

        product_service = ProductService()
        connection      = None

        try:
            connection = connect_db()
            result     = product_service.get_product_detail_list(connection, filters)

            return jsonify({"data": result})

        except Exception as e:
                connection.rollback()       
                raise e
        
        finally:
            if connection is not None:
                connection.close()