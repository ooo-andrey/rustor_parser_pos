import psycopg2

class data_base_connector:

    def __init__(self, url, user, password, db_name):
        self.url = url
        self.user = user
        self.password = password
        self.db_name = db_name

    # Открыть соединение с БД
    def open(self):

        try:
            connection = psycopg2.connect(
                host=self.url,
                user=self.user,
                password=self.password,
                database=self.db_name
            )

            connection.autocommit = True

            self.cursor = connection.cursor()

            return True

        except:
            return False

    # Закрыть соединение с БД
    def close(self):

        try:
            self.cursor.close()
            self.connection.close()
        except:
            return False
 
    # Отправить запрос в БД
    def make_request(self, sql_query):

        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()           
        except:
            return False 
