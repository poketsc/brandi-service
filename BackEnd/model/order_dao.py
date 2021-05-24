import pymysql
from util.const import END_DATE

class CartDao:

    # 카트에 상품 담기 기능
    def post_cart(self, data, connection):

        # 카트에 상품을 담는 sql문
        # product_option_id를 프론트로부터 받아오지 않아서 서브쿼리 사용으로 product_option_id 도출
        query  = """
            INSERT INTO carts(
                user_id,
                product_option_id,
                product_id
            )
            VALUES(
                %(user_id)s,
                %(product_option_id)s,
                ( SELECT
                    product_id
                FROM
                    product_options
                WHERE
                    id = %(product_option_id)s
                )
            )
        """
        
        with connection.cursor() as cursor:

            cursor.execute(query, data)

            result = cursor.lastrowid

            return result

    # 카트 히스토리에 담기 기능
    def post_history_cart(self, data, connection):
        data['END_DATE'] = END_DATE
        
        # 카트 히스토리에 데이터 담는 기능
        query = """ 
            INSERT INTO cart_histories(
                cart_id,
                quantity,
                start_time,
                end_time,
                is_deleted
            )
            VALUES (
                %(cart_id)s,
                %(quantity)s,
                %(now)s,
                %(END_DATE)s,
                false
            )
        """
    
        with connection.cursor() as cursor:

            result = cursor.execute(query, data)

            return result
        
    
    # 상품 옵션 판매 여부 확인
    def product_option_sold_out_check(self, data, connection):

        query = """
            SELECT 
                id,
                is_sold_out
            FROM
                product_options AS po
                
            WHERE
                po.id = %(product_option_id)s
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.fetchone()

            return result


    # 카트 정보 가져오기
    def get_cart_information(self, data, connection):

        query = """
            SELECT
                sh.korean_name,
                ph.name,
                ph.discount_rate,
                ph.price,
                co.color,
                s.size,
                po.color_id,
                po.size_id,
                ch.quantity,
                pi.image_url,
                c.product_id,
                c.product_option_id,
                ch.cart_id

            FROM carts as c

            JOIN products as p
            ON c.product_id = p.id

            JOIN product_histories as ph
            ON c.product_id = ph.product_id

            AND ph.is_deleted = false

            JOIN product_options as po
            ON c.product_option_id = po.id

            AND po.is_sold_out = false

            JOIN sizes as s
            ON po.size_id = s.Id

            JOIN colors as co
            ON po.color_id = co.Id

            JOIN cart_histories as ch
            ON c.id = ch.cart_id

            AND ch.is_deleted = false

            JOIN seller_histories as sh
            ON p.seller_id = sh.seller_id

            AND sh.is_deleted = false

            JOIN product_images as pi
            ON c.product_id = pi.product_id
            
            AND pi.is_main=true

            WHERE
                c.user_id=%(user_id)s
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.fetchall()

            return result

    # 카트 히스토리 선분이력 시간 끊기(end_time 시간 DB 기준 now로 설정)
    def update_cart_history_end_time(self, data, connection):
        data['END_DATE'] = END_DATE

        query = """
            UPDATE
                cart_histories AS ch

            INNER JOIN carts AS c
            ON c.id = ch.cart_id

            SET 
                ch.end_time = %(now)s,
                ch.is_deleted = true

            WHERE
                c.user_id = %(user_id)s
                AND c.product_option_id = %(product_option_id)s
                AND ch.end_time = %(END_DATE)s
                AND ch.is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            result = cursor.execute(query, data)

            return result
    
    # 카트 선분이력 복사,데이터 일괄 변경
    def update_cart_history_information(self, data, connection):
        data['END_DATE'] = END_DATE
        
        query = """
            INSERT INTO
                cart_histories (
                            cart_id,
                            start_time,
                            end_time,
                            quantity,
                            is_deleted
                            )
            SELECT
                cart_id,
                %(now)s,
                %(END_DATE)s,
                quantity + %(quantity)s,
                false

            FROM cart_histories AS ch

            INNER JOIN carts AS c
            ON c.id = ch.cart_id

            WHERE 
                c.user_id = %(user_id)s
                AND ch.end_time = %(now)s
                AND c.product_option_id = %(product_option_id)s
                AND ch.is_deleted = true
                AND quantity + %(quantity)s > 0
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            result = cursor.execute(query, data)

            return result