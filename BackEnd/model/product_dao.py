import pymysql
from util.const import END_DATE


class ProductDao:

    def get_product_list(self, connection, filters, is_count=False):
        """메인 상품 리스트

        Author:
            이서진

        Args:
            connection: 커넥션
            filters: 필터 조건
            is_count(boolean): 카운트 조건 여부

        Returns:
        """

        query = "SELECT"

        if is_count:
            query += " Count(*) AS count"

        elif not is_count:
            query += """
                p.Id AS id,
                pi.image_url AS image,
                ph.name AS name,
                ph.price AS price,
                ph.discount_rate AS discount_rate,
                ph.price - TRUNCATE((ph.price * (ph.discount_rate/100)), -1) AS sale_price,
                s.Id AS seller_id,
                sh.korean_name AS seller_name
            """

        query += f"""
            FROM products AS p
                INNER JOIN product_images AS pi
                    ON p.Id = pi.product_id
                INNER JOIN product_histories AS ph
                    ON p.Id = ph.product_id
                INNER JOIN sellers AS s
                    ON p.seller_id = s.Id
                INNER JOIN seller_histories AS sh
                    ON s.Id = sh.seller_id
            WHERE ph.is_deleted = false
              AND ph.end_time = '{END_DATE}'
              AND pi.is_main = true
        """

        if not is_count:
            query += " ORDER BY p.created_at DESC"
            query += " LIMIT %(offset)s, %(limit)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            product_list = cursor.fetchall()
            return product_list
