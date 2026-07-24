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



    def create_tables(self):

        try:
            self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Apps(
                    id serial PRIMARY KEY,
                    app_title VARCHAR(60) NOT NULL,
                    app_name VARCHAR(60) NOT NULL UNIQUE
                );
                
                CREATE TABLE IF NOT EXISTS Keys(
                    id serial PRIMARY KEY,
                    key VARCHAR(60) NOT NULL,
                    app_id INT NOT NULL,
                    UNIQUE (key, app_id)
                );

                CREATE TABLE IF NOT EXISTS RuStore(
                    id serial PRIMARY KEY,
                    app_id INT NOT NULL,
                    key_id INT NOT NULL,
                    pos INT,
                    date DATE NOT NULL
                );
                """
            )
        except:
            return print("sosi")


    def add_in_apps(self, app_title, app_name):

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

    def add_in_keys(self, key, app_name):

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
            return print("sosi 123")

    def add_in_rustore(self, app_name, key, pos, date):

        try:
            self.cursor.execute(
                f"""
                INSERT INTO RuStore(app_name, key, pos, date)
                VALUES('{app_name}', '{key}', {pos}, '{date}');
                """
            )
        except:
            return print("sosi") 

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
            return None

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
            return None        
    def close(self):

        try:
            self.cursor.close()
            self.connection.close()
            print("Close")
        except:
            return None
