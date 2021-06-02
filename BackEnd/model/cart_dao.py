import pymysql
from util.const import END_DATE

class CartDao:

    def post_cart(self, connection, filters):
        """카트에 상품 담기

        Author:
            백승찬

        Args:
            filters (dict): 사용자의 아이디, product_option_id 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:

        Returns:
            200 : lastrowid
        """

        query  = """
            INSERT INTO carts(
                user_id,
                product_option_id,
                product_id
            )
            VALUES(
                %(account_id)s,
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

            cursor.execute(query, filters)

            result = cursor.lastrowid

            return result

    def post_history_cart(self, connection, filters):
        """카트 히스토리에 담기 기능

        Author:
            백승찬

        Args:
            filters (dict): 사용자의 아이디, 다수의 cart_id, 다수의 quantity 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:

        Returns:
            200 : 1
        """
        
        # 카트 히스토리에 데이터 담는 기능
        query = f""" 
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
                "{END_DATE}",
                false
            )
        """
    
        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result

    # 카트 정보 가져오기
    def get_cart_information(self, connection, filters):
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
        
        query = f"""
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
                ch.cart_id,
                sh.seller_id,
                ph.price - TRUNCATE((ph.price * (ph.discount_rate/100)), -1) AS sale_price,
                TRUNCATE((ph.price * (ph.discount_rate/100)), -1) AS estimated_discount_price

            FROM
                carts as c

            INNER JOIN products as p
                    ON c.product_id = p.id
            INNER JOIN product_histories as ph
                    ON c.product_id = ph.product_id
                    AND ph.is_deleted = false
                    AND ph.end_time = "{END_DATE}"
            INNER JOIN product_options as po
                    ON c.product_option_id = po.id
                    AND po.is_sold_out = false
            INNER JOIN sizes as s
                    ON po.size_id = s.Id
            INNER JOIN colors as co
                    ON po.color_id = co.Id
            INNER JOIN cart_histories as ch
                    ON c.id = ch.cart_id
                    AND ch.is_deleted = false
                    AND ch.end_time = "{END_DATE}"
            INNER JOIN seller_histories as sh
                    ON p.seller_id = sh.seller_id
                    AND sh.is_deleted = false
                    AND sh.end_time = "{END_DATE}"
            INNER JOIN product_images as pi
                    ON c.product_id = pi.product_id
                    AND pi.is_main = true

            WHERE
                c.user_id = %(account_id)s
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchall()

            return result
    
    def get_cart_history_id_end_time(self, connection, filters):
        """cart_history_id 가져오기

        Author:
            백승찬

        Args:
            filters (dict): account_id, cart_id 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:

        Returns:
            200 : cart_history_id
        """

        query = f"""
            SELECT
                ch.id AS cart_history_id

            FROM
                cart_histories AS ch

            INNER JOIN carts AS c
                    ON c.id = ch.cart_id

            WHERE
                c.id              = %(cart_id)s
                AND c.user_id     = %(account_id)s
                AND ch.end_time   = "{END_DATE}"
                AND ch.is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result

    def update_cart_history_end_time(self, connection, filters):
        """카트 히스토리 선분이력 시간 끊기(end_time 시간 DB 기준 now로 설정)

        Author:
            백승찬

        Args:
            filters (dict): account_id, cart_id 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:

        Returns:
            200 : 1
        """

        query = f"""
            UPDATE
                cart_histories AS ch
            
            INNER JOIN carts AS c
                    ON c.id = ch.cart_id

            SET 
                end_time = %(now)s

            WHERE
                user_id        = %(account_id)s
                AND cart_id    = %(cart_id)s
                AND end_time   = "{END_DATE}"
                AND is_deleted = false
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result

    def update_cart_history_information(self, connection, filters):
        """카트 선분이력 복사,데이터 일괄 변경

        Author:
            백승찬

        Args:
            filters (dict): account_id, cart_id, cart_history_id, quantity(선택), is_deleted(선택) 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:

        Returns:
            200 : 1
        """
        
        query = f"""
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
                "{END_DATE}",
        """

        if not filters.get("quantity"):
            query += "quantity,"

        else:
            query += "%(quantity)s,"

        if not filters.get("is_deleted"):
            query += "false"
        
        else:
            query += "true"

        query += """
            FROM
                cart_histories AS ch
            
            INNER JOIN carts AS c
                    ON c.id = ch.cart_id

            WHERE
                user_id        = %(account_id)s
                AND cart_id    = %(cart_id)s
                AND ch.id      = %(cart_history_id)s
                AND is_deleted = false
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)
            
            return result