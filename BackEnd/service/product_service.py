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
