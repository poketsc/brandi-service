import pymysql

# now 클레스화 -> 재사용 하기위해서
class SelectNowDao:
    def select_now(self, connection):
        """현재 시점 선언

        - 이력 관리를 위한 now 시점 선언

        Author:
            백승찬

        Args:
            connection (객체): pymysql 객체

        Raises:

        Returns:
            200 :  datetime.datetime()
        """

        query = """
            SELECT now()
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(query)

            result = cursor.fetchone()
            result = result["now()"]

            return result