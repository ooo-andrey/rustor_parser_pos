
# Создать все нужные таблицы
create_tables = f"""
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


# Добавить запись в таблицу Apps
def add_apps(app_title, app_name):

    return f"""
        INSERT INTO Apps(app_title, app_name)
        VALUES('{app_title}', '{app_name}')
    """

# Добавить запись в таблицу Markets
def add_markets(market_name):

    return f"""
        INSERT INTO Markets(market_name)
        VALUES('{market_name}')
    """

# Добавить запись в таблицу Keys
def add_keys(key, app_name):

    return f"""
        INSERT INTO Keys(key, app_id)
        VALUES('{key}',
        (SELECT id FROM Apps WHERE app_name = '{app_name}'));
    """

# Добавить запись в таблицу Stats
def add_stats(app_id, key_id, market_id, pos, date):

    return f"""
        INSERT INTO Stats(app_id, key_id, market_id, position, date)
        VALUES({app_id}, '{key_id}', {market_id}, {pos}, '{date}');
    """

# Получить id ключа
def get_key_id(key, app_id): 

    return f"""
        SELECT id
        FROM Keys
        WHERE key = '{key}' AND app_id = {app_id};
    """

# Получить все ключевые слова по определенному приложению
def get_keys(app_name):

    return f"""
        SELECT key
        FROM Keys
        WHERE app_id = (SELECT id FROM Apps WHERE app_name = '{app_name}');
    """

 # Получить название приложения
def get_app_name(app_title):

    return f"""
        SELECT app_name
        FROM Apps
        WHERE app_title = '{app_title}';
    """

# Получить id приложения
def get_app_id(app_name):

    return f"""
        SELECT id
        FROM Apps
        WHERE app_name = '{app_name}';
    """
