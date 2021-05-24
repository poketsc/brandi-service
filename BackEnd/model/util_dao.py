import pymysql

# now 클레스화 -> 재사용 하기위해서
class SelectNowDao:
    def select_now(self, connection):

        query = """
            SELECT now()
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query)

            result = cursor.fetchone()

            result = result['now()']

            return result