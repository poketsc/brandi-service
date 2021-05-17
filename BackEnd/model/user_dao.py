import pymysql

#################################초기세팅#############################
class TestDao:
    
    def post_test(self, data, connection):

        insert_data = "insert into test(name) values(%(name)s)"

        with connection.cursor() as cursor:

            cursor.execute(insert_data, {'name' : data['name']})

            results = cursor.lastrowid
            return results

class UserDao:
    def get_test(self, connection):
        sql = "select * from test"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)

            test_list = cursor.fetchall()
            
            return test_list
#################################초기세팅#############################