import psycopg2


class DATABASE:
    host = "192.168.1.156"
    user = "admin"
    password = "admin123"
    db_name = "testdb"

    def open(self):

        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )

            connection.autocommit = True

            self.cursor = connection.cursor()

        except:
            return None



    def create_table(self):

        try:
            self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS RuStore(
                    id serial PRIMARY KEY,
                    app_name VARCHAR(40) NOT NULL,
                    key VARCHAR(40) NOT NULL,
                    pos INT NOT NULL,
                    date DATE NOT NULL
                );
                """
            )
        except:
            return None

    def add_key_pos(self, app_name, key, pos, date):

        try:
            self.cursor.execute(
                f"""
                INSERT INTO RuStore(app_name, key, pos, date)
                VALUES('{app_name}', '{key}', {pos}, '{date}')
                """
            )
        except:
            return print("sosi") 

    def close(self):

        try:
            self.cursor.close()
            self.connection.close()
            print("Close")
        except:
            return None
