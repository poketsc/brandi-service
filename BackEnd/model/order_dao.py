import pymysql
from util.const import END_DATE, PAYMENT_COMPLETE, ORDER_COMPLETE

class OrderDao:

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