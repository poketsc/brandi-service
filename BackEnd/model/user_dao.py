import pymysql

#################################초기세팅#############################
class TestDao:
    
    def post_test(self, data, connection):

        insert_data = """INSERT INTO sizes(size) 
                        VALUES (%(size)s)"""

        with connection.cursor() as cursor:

            cursor.execute(insert_data, data)

            return cursor.lastrowid

class UserDao:
    def get_test(self, connection):
        sql = "SELECT * FROM users"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)

            test_list = cursor.fetchall()
            
            return test_list
#################################초기세팅#############################