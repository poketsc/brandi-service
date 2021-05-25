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

class OrderDao:

    def get_defaulted_true_shipment_information(self, data, connection):

        query = """
            SELECT 
                ah.id,
                address_id,
                name,
                phone_number,
                address

            FROM  address_histories AS ah

            INNER JOIN addresses AS ad
            ON ad.id = ah.address_id

            WHERE user_id = %(user_id)s
            AND is_defaulted = true;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.fetchone()

            return result
            
    def get_shipment_memo_information(self, connection):

        query = """
            SELECT 
                id,
                content
            FROM shipment_memo
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query)

            result = cursor.fetchall()

            return result
    
    def get_address_id(self, data, connection):

        query = """
            SELECT
                id
            
            FROM
                addresses
            
            WHERE
                user_id = %(user_id)s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.fetchall()

            return result
            
    def insert_shipment_information(self, data, connection):
        data['END_DATE'] = END_DATE

        query = """
            INSERT INTO shipments (
                order_id,
                order_product_id,
                address_id,
                shipment_status_id,
                shipment_memo_id,
                message
                )
            VALUES (
                %(order_id)s,
                %(order_product_id)s,
                %(address_id)s,
                1,
                %(shipment_memo_id)s,
                %(message)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            result = cursor.execute(query, data)

            return result

    def insert_order_information(self, data, connection):

        query = """
            INSERT INTO orders (
                user_id,
                created_at
                )
            VALUES (
                %(user_id)s,
                %(now)s
            )
        """

        with connection.cursor() as cursor:

            cursor.execute(query, data)

            result = cursor.lastrowid

            return result
    
    def insert_order_history_information(self, data, connection):
        data['END_DATE'] = END_DATE
        
        query = """
            INSERT INTO order_histories (
                payment_status_id,
                order_id,
                start_time,
                end_time,
                total_price,
                is_canceled,
                orderer_name,
                orderer_phone_number,
                orderer_email
            )
            VALUES (
                2,
                %(order_id)s,
                %(now)s,
                %(END_DATE)s,
                %(total_price)s,
                false,
                %(orderer_name)s,
                %(orderer_phone_number)s,
                %(orderer_email)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.lastrowid

            return result

    
    def insert_order_product_information(self, data, connection):

        query = """
            INSERT INTO order_products (
                order_id,
                product_option_id,
                product_id
            )
            VALUES (
                %(order_id)s,
                %(product_option_id)s,
                %(product_id)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.lastrowid

            return result

    def insert_order_product_history_information(self, data, connection):
        data['END_DATE'] = END_DATE

        query = """
            INSERT INTO order_product_histories (
                order_status_id,
                order_product_id,
                start_time,
                end_time,
                is_canceled,
                price,
                quantity )
            VALUES (
                1,
                %(order_product_id)s,
                %(now)s,
                %(END_DATE)s,
                false,
                %(price)s,
                %(quantity)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            result = cursor.execute(query, data)

            return result

class ShipmentDao:

    def get_all_shipment_information(self, data, connection):

        query = """
            SELECT
                address_id,
                start_time,
                end_time,
                name,
                phone_number,
                is_deleted,
                is_defaulted,
                address

            FROM
                address_histories as ah

            INNER JOIN addresses as ad
            ON ad.id = ah.address_id
            
            WHERE ad.user_id = %(user_id)s
            AND ah.is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, data)

            result = cursor.fetchall()

            return result
    
    def insert_address_information(self, data, connection):

        query = """
            INSERT INTO addresses (
                user_id
            )
            VALUES (
                %(user_id)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            cursor.execute(query, data)

            result = cursor.lastrowid

            return result
    
    # 주소 업데이트 시간 끊기
    def update_address_history_end_time(self, data, connection):

        query = """
            UPDATE
                address_histories
            
            SET
                end_time = %(now)s,
                is_defaulted = false
            
            WHERE
                address_id = %(address_id)s
                AND is_defaulted = true
                AND is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            result = cursor.execute(query, data)

            return result
    
    # 주소 추가
    def insert_address_history_information(self, data, connection):
        data['END_DATE'] = END_DATE

        query = """
            INSERT INTO
                address_histories (
                    address_id,
                    start_time,
                    end_time,
                    name,
                    phone_number,
                    is_deleted,
                    is_defaulted,
                    address
                )
            VALUES (
                %(address_id)s,
                %(now)s,
                %(END_DATE)s,
                %(name)s,
                %(phone_number)s,
                false,
                %(is_defaulted)s,
                %(address)s
                )
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, data)

            return result