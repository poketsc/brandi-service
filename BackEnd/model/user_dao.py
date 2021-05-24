import pymysql

from util.const import USER_ACCOUNT_TYPE

class SignInDao:
    def get_user_info(self, connection, data):
        query = f"""
            SELECT 
                a.id,
                a.account_type_id,
                a.nickname,
                uh.password
            FROM accounts AS a
            INNER JOIN users AS u
                ON a.id = u.id
            INNER JOIN user_histories AS uh
                ON u.id = uh.user_id
            WHERE a.nickname = %(nickname)s
                AND a.account_type_id = {USER_ACCOUNT_TYPE}
                AND uh.is_deleted = 0
                """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)

            return cursor.fetchall()