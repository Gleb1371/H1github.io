import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port=3305,
    user="root",
    password="informatika2307",
    database="Hainan",
)

cursor = connection.cursor()

# # Данные администратора
# admin_data = ("login", "password", "name", "89953477278", "admin")

# # SQL-запрос для добавления администратора
# add_admin = """
# INSERT INTO users (login, password, first_name, phone_number, role)
# VALUES (%s, %s, %s, %s, %s)
# """

# # Выполнение SQL-запроса для добавления администратора
# cursor.execute(add_admin, admin_data)

# # Данные преподавателя
# teacher_data = ("login", "password", "name", "89983457385", "teacher")

# # SQL-запрос для добавления преподавателя
# add_teacher = """
# INSERT INTO users (login, password, first_name, phone_number, role)
# VALUES (%s, %s, %s, %s, %s)
# """

# Выполнение SQL-запроса для добавления преподавателя
#cursor.execute(add_teacher, teacher_data)

# Данные клиента для добавления
#client_data = ("Иван", "12345678901", "classes")

# SQL-запрос для добавления клиента
# add_client = """
# INSERT INTO clients (first_name, phone_number, role)
# VALUES (%s, %s, %s)
# """

# cursor.execute(add_client, client_data)

# client_data = ("Степан", "12345678900", "trips")

# # SQL-запрос для добавления клиента
# add_client = """
# INSERT INTO clients (first_name, phone_number, role)
# VALUES (%s, %s, %s)
# """

# # Выполнение SQL-запроса для добавления клиента
# cursor.execute(add_client, client_data)

# SQL-запрос для извлечения имен всех администраторов
sql_query = """
SELECT first_name
FROM users
WHERE role = 'admin'
"""

# Выполнение SQL-запроса
cursor.execute(sql_query)

# Получение результатов запроса
admins = cursor.fetchall()

print("Имена всех администраторов:")
for admin in admins:
    print(admin[0])
    
sql_query = """
SELECT first_name, phone_number
FROM clients
WHERE role = 'trips'
"""

# Выполнение SQL-запроса
cursor.execute(sql_query)

# Получение результатов запроса
clientss = cursor.fetchall()

print("Имена и номера телефонов всех клиентов (поездки):")
for client in clientss:
    print(client[0], client[1])

# Подтверждение изменений в базе данных
connection.commit()

# Закрытие соединения
cursor.close()
connection.close()