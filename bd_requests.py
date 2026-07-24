import psycopg2


class DATABASE:

    host = "192.168.1.156"
    user = "admin"
    password = "admin123"
    db_name = "testdb"

    # Открыть соединение с БД
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

    # Закрыть соединение с БД
    def close(self):

        try:
            self.cursor.close()
            self.connection.close()
            print("Close")
        except:
            return None

    # Создать все нужные таблицы
    def create_tables(self):

        try:
            self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Apps(
                    id serial PRIMARY KEY,
                    app_title VARCHAR(60) NOT NULL,
                    app_name VARCHAR(60) NOT NULL UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Markets(
                    id serial PRIMARY KEY,
                    market_name VARCHAR(60) NOT NULL UNIQUE
                );
                
                CREATE TABLE IF NOT EXISTS Keys(
                    id serial PRIMARY KEY,
                    key VARCHAR(60) NOT NULL,
                    app_id INT NOT NULL,
                    UNIQUE (key, app_id)
                );

                CREATE TABLE IF NOT EXISTS Stats(
                    id serial PRIMARY KEY,
                    app_id INT NOT NULL,
                    key_id INT NOT NULL,
                    market_id INT NOT Null,
                    position INT,
                    date DATE NOT NULL
                );
                """
            )
        except:
            return False

    # Добавить запись в таблицу Apps
    def add_apps(self, app_title, app_name):

        try:
            self.cursor.execute(
                f"""
                INSERT INTO Apps(app_title, app_name)
                VALUES('{app_title}', '{app_name}')
                """
            )
            return True
        except:
            return False

    # Добавить запись в таблицу Markets
    def add_markets(self, market_name):

        try:
            self.cursor.execute(
                f"""
                INSERT INTO Markets(market_name)
                VALUES('{market_name}')
                """
            )
            return True
        except:
            return False

    # Добавить запись в таблицу Keys
    def add_keys(self, key, app_name):

        try:
            self.cursor.execute(
                f"""
                INSERT INTO Keys(key, app_id)
                VALUES('{key}',
                       (SELECT id FROM Apps WHERE app_name = '{app_name}'));
                """
            )
            return True
        except:
            return False
        
    # Добавить запись в таблицу Stats
    def add_stats(self, app_id, key_id, market_id, pos, date):

        try:
            self.cursor.execute(
                f"""
                INSERT INTO Stats(app_id, key_id, market_id, position, date)
                VALUES({app_id}, '{key_id}', {market_id}, {pos}, '{date}');
                """
            )
        except:
            return print("sosite")

    # Получить все ключевые слова по определенному приложению
    def get_keys(self, app_name):

        try:
            self.cursor.execute(
                f"""
                SELECT key
                FROM Keys
                WHERE app_id = (SELECT id FROM Apps WHERE app_name = '{app_name}');
                """
            )        

            return [key[0] for key in self.cursor.fetchall()]
        except:
            return False

    # Получить название приложения
    def get_app_name(self, app_title):

        try:
            self.cursor.execute(
                f"""
                SELECT app_name
                FROM Apps
                WHERE app_title = '{app_title}';
                """
            )        

            return [key[0] for key in self.cursor.fetchall()]
        except:
            return False 

    # Получить id приложения
    def get_app_id(self, app_name):

        try:
            self.cursor.execute(
                f"""
                SELECT id
                FROM Apps
                WHERE app_name = '{app_name}';
                """
            )        

            return [key[0] for key in self.cursor.fetchall()][0]
        except:
            return False   

    # Получить id ключа
    def get_key_id(self, key, app_id):

        try:
            self.cursor.execute(
                f"""
                SELECT id
                FROM Keys
                WHERE key = '{key}' AND app_id = {app_id};
                """
            )        

            return [key[0] for key in self.cursor.fetchall()][0]
        except:
            return False   
