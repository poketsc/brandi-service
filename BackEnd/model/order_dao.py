import pymysql
from util.const import END_DATE, PAYMENT_COMPLETE, ORDER_COMPLETE, SHIPMENT_READY

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
    
    # 상품 존재 여부 확인
    def product_exist_check(self, connection, filters):

        query = """
            SELECT
                ph.id
            
            FROM
                product_histories AS ph
        """

        if filters.get("cart_id"):
            query += f"""
                INNER JOIN carts AS c
                        ON c.product_id = ph.product_id

                WHERE
                    c.id = %(cart_id)s
                    AND ph.end_time = "{END_DATE}"
                    AND ph.is_deleted = false
                    AND ph.is_sold = true
            """

        if filters.get("product_option_id"):
            query += f"""
                INNER JOIN product_options AS po
                        ON po.product_id = ph.product_id

                WHERE
                    po.id = %(product_option_id)s
                    AND ph.end_time = "{END_DATE}"
                    AND ph.is_deleted = false
                    AND ph.is_sold = true
            """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result
        
    # 상품 옵션 판매 여부 확인
    def product_option_sold_out_check(self, connection, filters):

        query = """
            SELECT 
                po.id
            FROM
                product_options AS po
        """

        if filters.get("cart_id"):
            query += """
                INNER JOIN carts AS c
                        ON c.product_option_id = po.id
                WHERE
                    c.id = %(cart_id)s
                    AND po.is_sold_out = false
            """
        
        if filters.get("product_option_id"):
            query += """
                WHERE
                    po.id = %(product_option_id)s
                    AND po.is_sold_out = false
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
    
    def get_cart_history_id_end_time(self, connection, filters):

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

    # 카트 히스토리 선분이력 시간 끊기(end_time 시간 DB 기준 now로 설정)
    def update_cart_history_end_time(self, connection, filters):

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

class OrderDao:

    def get_defaulted_true_shipment_information(self, connection, filters):

        query = f"""
            SELECT 
                ah.id AS address_history_id,
                address_id,
                name,
                phone_number,
                address,
                additional_address,
                zip_code,
                is_deleted

            FROM
                address_histories AS ah

            INNER JOIN addresses AS ad
                    ON ad.id = ah.address_id

            WHERE
                user_id          = %(account_id)s
                AND end_time     = "{END_DATE}"
                AND is_deleted   = false
                AND is_defaulted = true
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result
            
    def get_shipment_memo_information(self, connection):

        query = """
            SELECT 
                id,
                content

            FROM
                shipment_memo
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query)

            result = cursor.fetchall()

            return result

    def get_orderer_information(self, connection, filters):

        query = """
            SELECT
                oh.orderer_name,
                oh.orderer_phone_number,
                oh.orderer_email

            FROM
                order_histories AS oh

            INNER JOIN orders AS o
                    ON o.id = oh.order_id

            WHERE o.user_id = %(account_id)s

            ORDER BY o.created_at DESC
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

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
    
    def get_discount_product_check(self, connection, filters):

        query = f"""
            SELECT
                ph.price - TRUNCATE((ph.price * (ph.discount_rate/100)), -1) AS sale_price

            FROM product_histories AS ph

            WHERE
                ph.product_id     = %(product_id)s
                AND ph.is_sold    = true
                AND ph.end_time   = "{END_DATE}"
                AND ph.is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result

    def insert_shipment_information(self, connection, filters):

        query = f"""
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
                "{SHIPMENT_READY}",
                %(shipment_memo_id)s,
                %(message)s
            )
        """
        
        with connection.cursor() as cursor:
            
            result = cursor.execute(query, filters)

            return result

    def insert_order_information(self, connection, filters):

        query = """
            INSERT INTO orders (
                user_id,
                created_at
                )
            VALUES (
                %(account_id)s,
                %(now)s
            )
        """

        with connection.cursor() as cursor:

            cursor.execute(query, filters)

            result = cursor.lastrowid

            return result
    
    def insert_order_history_information(self, connection, filters):
        
        query = f"""
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
                "{PAYMENT_COMPLETE}",
                %(order_id)s,
                %(now)s,
                "{END_DATE}",
                %(total_price)s,
                false,
                %(orderer_name)s,
                %(orderer_phone_number)s,
                %(orderer_email)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.lastrowid

            return result

    
    def insert_order_product_information(self, connection, filters):

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

            cursor.execute(query, filters)

            result = cursor.lastrowid

            return result

    def insert_order_product_history_information(self, connection, filters):

        query = f"""
            INSERT INTO order_product_histories (
                order_status_id,
                order_product_id,
                start_time,
                end_time,
                is_canceled,
                quantity,
                price
            )

            SELECT 
                "{ORDER_COMPLETE}",
                %(order_product_id)s,
                %(now)s,
                "{END_DATE}",
                false,
                ch.quantity,
        """

        if filters.get("sale_price"):
            query += "%(sale_price)s"
        
        else:
            query += "ch.price"

        query += f"""
            FROM
                carts AS c
            
            INNER JOIN cart_histories AS ch
                    ON c.id = ch.cart_id
            INNER JOIN product_histories AS ph
                    ON ph.product_id  = c.product_id
                    AND ph.is_sold    = true
                    AND ph.end_time   = "{END_DATE}"
                    AND ph.is_deleted = false
            
            WHERE
                c.user_id = %(account_id)s
                AND c.id  = %(cart_id)s
                AND c.product_option_id = %(product_option_id)s
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result
    
    def update_product_option_stock(self, connection, filters):

        query = """
            UPDATE
                product_options

            SET
                stock = stock - %(quantity)s

            WHERE
                id = %(product_option_id)s
                AND stock - %(quantity)s > -11
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result
    
    def update_product_option_is_sold_out(self, connection, filters):

        query = """
            UPDATE
                product_options

            SET
                is_sold_out = true

            WHERE
                id        = %(product_option_id)s
                AND stock = -10
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result

    def get_order_complete_information(self, connection, filters):

        query = """
            SELECT
                o.id,
                oh.total_price
            
            FROM
                order_histories AS oh
            
            INNER JOIN orders AS o
                    ON o.id = oh.order_id
            
            WHERE
                user_id  = %(account_id)s
                AND o.id = %(order_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result

class ShipmentDao:

    def get_all_shipment_information(self, connection, filters):

        query = f"""
            SELECT
                ah.id AS address_history_id,
                ad.id AS address_id,
                start_time,
                end_time,
                name,
                phone_number,
                is_deleted,
                is_defaulted,
                address,
                additional_address,
                zip_code

            FROM
                address_histories as ah

            INNER JOIN addresses as ad
                    ON ad.id = ah.address_id
            
            WHERE
                ad.user_id        = %(account_id)s
                AND ah.is_deleted = false
                AND ah.end_time   = "{END_DATE}"
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchall()

            return result

    def get_one_shipment_information(self, connection, filters):

        query = f"""
            SELECT
                address_id,
                start_time,
                end_time,
                name,
                phone_number,
                is_deleted,
                is_defaulted,
                address,
                additional_address,
                zip_code

            FROM
                address_histories AS ah

            INNER JOIN addresses AS a
                    ON a.id = ah.address_id

            WHERE a.user_id   = %(account_id)s
            AND ah.address_id = %(address_id)s
            AND ah.end_time   = "{END_DATE}"
            AND ah.is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query, filters)

            result = cursor.fetchone()

            return result
    
    def insert_address_information(self, connection, filters):

        query = """
            INSERT INTO addresses (
                user_id
            )
            VALUES (
                %(account_id)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            cursor.execute(query, filters)

            result = cursor.lastrowid

            return result
    
    # 주소 업데이트 시간 끊기
    def update_address_history_end_time(self, connection, filters):

        query = f"""
            UPDATE
                address_histories AS ah
            
            INNER JOIN addresses AS a
                    ON a.id = ah.address_id
            
            SET
                end_time = %(now)s
            
            WHERE
                a.id              = %(address_id)s
                AND a.user_id     = %(account_id)s
                AND ah.end_time   = "{END_DATE}"
                AND ah.is_deleted = false
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result
    
    # 주소 히스토리 추가
    def insert_address_history_information(self, connection, filters):
        
        query = f"""
            INSERT INTO
                address_histories (
                    address_id,
                    start_time,
                    end_time,
                    name,
                    phone_number,
                    is_deleted,
                    is_defaulted,
                    address,
                    additional_address,
                    zip_code
            )
            VALUES (
                %(address_id)s,
                %(now)s,
                "{END_DATE}",
                %(name)s,
                %(phone_number)s,
                %(is_deleted)s,
                %(is_defaulted)s,
                %(address)s,
                %(additional_address)s,
                %(zip_code)s
            )
        """

        with connection.cursor() as cursor:

            result = cursor.execute(query, filters)

            return result