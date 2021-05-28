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

        if filters.get("product_id"):
            query += """
                AND ph.product_id != %(product_id)s
                AND sh.seller_id = %(seller_id)s
            """

        if not is_count:
            query += " ORDER BY p.created_at DESC"
            query += " LIMIT %(offset)s, %(limit)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            product_list = cursor.fetchall()
            return product_list

    def get_product_detail(self, filters, connection):

        query = """
            SELECT
                sh.seller_id,
                sh.korean_name,
                ph.name,
                ph.price,
                ph.discount_rate,
                ph.price - TRUNCATE((ph.price * (ph.discount_rate/100)), -1) AS sale_price,
                (   
                    SELECT
                        COUNT(*)
                    FROM
                        order_product_histories AS oh
                    INNER JOIN order_products AS op
                            ON op.id = oh.order_product_id
                    WHERE
                        op.product_id = %(product_id)s
                    AND
                        oh.order_status_id = 1
                ) AS total_order,
                ph.shipment_information,
                ph.detail_page_html

            FROM product_histories AS ph

            INNER JOIN products AS p
                    ON p.id = ph.product_id

            INNER JOIN seller_histories AS sh
                    ON sh.seller_id = p.seller_id

            WHERE
                ph.product_id = %(product_id)s                  
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result

    def get_product_image(self, filters, connection):

        query = """
            SELECT     
                image_url,
                is_main
            FROM
                product_images
            WHERE
                product_id = %(product_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchall()

            return result
    
    def get_product_option_information(self, filters, connection):
        
        query = """
            SELECT
                po.id,
                s.size,
                c.color
            FROM
                product_options AS po
            INNER JOIN sizes AS s
                    ON po.size_id = s.id
            INNER JOIN colors AS c
                    ON po.color_id = c.id
            WHERE
                po.product_id      = %(product_id)s
                AND po.is_sold_out = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchall()

            return result