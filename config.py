from bd_requests import data_base 

# Создаем бд если её нет
bd = data_base("192.168.1.156", "admin", "admin123", "testdb")

bd.open()
bd.create_tables()
bd.close()
