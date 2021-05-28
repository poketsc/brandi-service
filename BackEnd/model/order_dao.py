import pymysql
from util.const import END_DATE

class CartDao:

    # 카트에 상품 담기 기능
    def post_cart(self, connection, filters):

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

    # 카트 히스토리에 담기 기능
    def post_history_cart(self, connection, filters):
        
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
        
    # 상품 옵션 판매 여부 확인
    def product_option_sold_out_check(self, connection, filters):

        query = """
            SELECT 
                po.id,
                po.is_sold_out
            FROM
                product_options AS po
        """

        if filters.get("cart_id"):
            query += """
                INNER JOIN carts AS c
                        ON c.product_option_id = po.id
                WHERE
                    c.id = %(cart_id)s
            """
        
        if filters.get("product_option_id"):
            query += """
                WHERE
                    po.id = %(product_option_id)s
            """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result

    # 카트 정보 가져오기
    def get_cart_information(self, connection, filters):

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

    # 카트 히스토리 선분이력 시간 끊기(end_time 시간 DB 기준 now로 설정)
    def update_cart_history_end_time(self, connection, filters):

        query = f"""
            UPDATE
                cart_histories

            SET 
                end_time = %(now)s

            WHERE
                cart_id              = %(cart_id)s
                AND end_time         = "{END_DATE}"
                AND is_deleted       = false
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result
    
    # 카트 선분이력 복사,데이터 일괄 변경
    def update_cart_history_information(self, connection, filters):
        
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

        if filters.get("quantity"):
            query += "quantity + %(quantity)s,"

        if not filters.get("is_deleted"):
            query += "false"
        
        if filters.get("is_deleted"):
            query += "true"

        query += """
            FROM
                cart_histories AS ch

            WHERE 
                cart_id        = %(cart_id)s
                AND end_time   = %(now)s
                AND is_deleted = false
        """

        if filters.get("quantity"):
            query += "AND quantity + %(quantity)s > 0"
        
        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)
            
            return result

class OrderDao:

    def get_defaulted_true_shipment_information(self, data, connection):
        data['END_DATE'] = END_DATE

        query = """
            SELECT 
                ah.id,
                address_id,
                name,
                phone_number,
                address,
                is_deleted,
                is_defaulted

            FROM address_histories AS ah

            INNER JOIN addresses AS ad
            ON ad.id = ah.address_id

            WHERE user_id = %(user_id)s
            AND ah.end_time = %(END_DATE)s
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
        data['END_DATE'] = END_DATE

        query = """
            SELECT
                ah.id
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
            AND ah.is_deleted = falseㅌ
            AND ah.end_time = %(END_DATE)s
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
                is_defaulted = %(is_defaulted)s,
                is_deleted = %(is_deleted)s
            
            WHERE
                id = %(id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            result = cursor.execute(query, data)

            return result
    
    # 주소 히스토리 추가
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
                %(is_deleted)s,
                %(is_defaulted)s,
                %(address)s
                )
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, data)

            return result