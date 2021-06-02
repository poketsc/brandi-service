import pymysql
from util.const import END_DATE, SHIPMENT_READY

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
    
    def insert_shipment_information(self, connection, filters):

        query = """
            INSERT INTO shipments (
                order_id,
                order_product_id,
                shipment_status_id,
                shipment_memo_id
        """

        if filters.get("message"):
            query += """
                ,message )
            """
        else:
            query += ")"

        query += f"""
            VALUES (
                %(order_id)s,
                %(order_product_id)s,
                "{SHIPMENT_READY}",
                %(shipment_memo_id)s
        """

        if filters.get("message"):
            query += """
                ,%(message)s )
            """
        else:
            query += ")"

        with connection.cursor() as cursor:
            
            cursor.execute(query, filters)

            result = cursor.lastrowid

            return result

    def insert_shipment_history_information(self, connection, filters):

        query = f"""
            INSERT INTO shipment_histories (
                shipment_id,
                address,
                additional_address,
                zip_code,
                phone_number,
                name,
                start_time,
                end_time
            )
            VALUES (
                %(shipment_id)s,
                %(address)s,
                %(additional_address)s,
                %(zip_code)s,
                %(phone_number)s,
                %(name)s,
                %(now)s,
                "{END_DATE}"
            )
        """

        with connection.cursor() as cursor:
            
            result = cursor.execute(query, filters)

            return result