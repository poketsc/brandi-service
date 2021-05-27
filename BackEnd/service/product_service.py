from model import ProductDao


class ProductService:

    def get_product_list(self, connection, filters):
        """메인 상품 리스트

        Author:
            이서진

        Args:
            connection: DB 커넥션
            filters: 쿼리 필터 조건

        Returns:
        """

        product_dao = ProductDao()
        products = product_dao.get_product_list(connection, filters)
        count = product_dao.get_product_list(connection, filters, is_count=True)

        return {"products": products, "count": count[0]["count"]}
    
    def get_product_detail_list(self, filters, connection):

        product_dao = ProductDao()

        product_detail             = product_dao.get_product_detail(filters, connection)
        product_image              = product_dao.get_product_image(filters, connection)
        product_option_information = product_dao.get_product_option_information(filters, connection)

        # 셀러 아이디 filters에 추가
        filters["seller_id"] = product_detail[0]["seller_id"]

        product_list = product_dao.get_product_list(connection, filters)

        result = {
            "product_detail"             : product_detail,
            "product_image"              : product_image,
            "product_option_information" : product_option_information,
            "related_product_list"       : product_list
        }

        return result