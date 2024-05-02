from fastapi import FastAPI 
from pydantic import BaseModel 
from fastapi import HTTPException 
import mysql.connector
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "praktika2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90  # Время жизни токена в минутах
 
app = FastAPI() 
 
connection = mysql.connector.connect( 
    host="localhost", 
    port=3305, 
    user="root", 
    password="informatika2307", 
    database="hainan", 
)  
 
# -------для таблицы USERS 
class user_log(BaseModel): 
    login: str
    password: str
    first_name: str
    phone_number: str  
    role: str
 
# ------------------------ТАБЛИЦА USERS------------------------------- 
# Получить список всех пользователей 
@app.get("/users") 
def get_users(): 
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM users") 
    result = cursor.fetchall()  # возвращаем все строки в виде списка 
    cursor.close() 
    return {"users": result} 
  
# Получить информацию о пользователе по ID 
@app.get("/users/{id}") 
def get_user_by_id(id: int): 
    cursor = connection.cursor() 
    cursor.execute(f"SELECT * FROM users WHERE id = {id}") 
    result1 = ( 
        cursor.fetchone() 
    )  # возвращает следующую строку результата запроса как кортеж 
    return {"User": result1} 
  
# Удалить пользователя по ID 
@app.delete("/users/{id}") 
def delete_user_by_id(id: int): 
    cursor = connection.cursor() 
    cursor.execute(f"SELECT * FROM users WHERE id = {id}") 
    result = cursor.fetchone() 
    if result: 
        cursor.execute(f"DELETE FROM users WHERE id = {id}") 
        connection.commit() 
        return {"message": "Пользователь удалён"} 
    else: 
        return {"message": "Пользователь не найден"}  
  
# Добавить пользователя
@app.post("/users")
def create_user(user: user_log):
    cursor = connection.cursor()
    # Проверяем, существует ли уже пользователь с таким логином
    cursor.execute(
        "SELECT * FROM users WHERE login = %s",
        (user.login,)
    )
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")

    # Если такого пользователя нет, добавляем нового пользователя
    cursor.execute(
        "INSERT INTO users (login, password, first_name, phone_number, role) VALUES (%s, %s, %s, %s, %s)",
        (user.login, user.password, user.first_name, user.phone_number, user.role)
    )
    connection.commit()  # Подтверждение транзакции
    cursor.close()
    return {"message": "Пользователь успешно создан"}


# Редактировать пользователя по ID
@app.put("/users/{id}")
def update_user(id: int, user_update: user_log):
    cursor = connection.cursor()
    # Проверяем, существует ли пользователь с указанным ID
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    existing_user = cursor.fetchone()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Выполняем SQL-запрос для обновления данных пользователя
    cursor.execute(
        "UPDATE users SET login = %s, password = %s, first_name = %s, phone_number = %s, role = %s WHERE id = %s",
        (user_update.login, user_update.password, user_update.first_name, user_update.phone_number, user_update.role, id)
    )
    connection.commit()  # Подтверждение транзакции
    cursor.close()

    return {"message": "Пользователь успешно обновлен"}

# Модель данных для входа пользователя
class UserLogin(BaseModel):
    login: str
    password: str

# Вход пользователя
@app.post("/users/login")
def login_user(user_data: UserLogin):
    cursor = connection.cursor()
    # Поиск пользователя по логину и паролю
    sql = "SELECT id FROM users WHERE login = %s AND password = %s"
    val = (user_data.login, user_data.password)
    cursor.execute(sql, val)
    id = cursor.fetchone()

    if not id:
        raise HTTPException(
            status_code=400, detail="Неверный логин или пароль"
        )

    access_token = generate_access_token(id)

    return {"access_token": access_token, "token_type": "Bearer", "message": "Вход выполнен успешно"}

# Генерация токена доступа
def generate_access_token(id: int):
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(id), "exp": expiration_time}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

# ------------------------ТАБЛИЦА CLIENTS------------------------------- 

# Модель данных для клиента
class Client(BaseModel):
    first_name: str
    phone_number: str
    role: str

# Получить список всех клиентов
@app.get("/clients")
def get_clients():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients")
    result = cursor.fetchall()
    cursor.close()
    return {"clients": result}

# Получить информацию о клиенте по ID
@app.get("/clients/{id}")
def get_client_by_id(id: int):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM clients WHERE id = {id}")
    result = cursor.fetchone()
    cursor.close()
    if not result:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return result

# Удалить клиента по ID
@app.delete("/clients/{id}")
def delete_client_by_id(id: int):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM clients WHERE id = {id}")
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    cursor.execute(f"DELETE FROM clients WHERE id = {id}")
    connection.commit()
    cursor.close()
    return {"message": f"Клиент с ID {id} удален"}

# Добавить клиента
@app.post("/clients")
def create_client(client: Client):
    cursor = connection.cursor()
    # Проверяем, существует ли клиент с такими же данными
    cursor.execute(
        "SELECT * FROM clients WHERE first_name = %s AND phone_number = %s AND role = %s",
        (client.first_name, client.phone_number, client.role)
    )
    existing_client = cursor.fetchone()
    if existing_client:
        cursor.close()
        raise HTTPException(status_code=400, detail="Клиент с этими данными уже существует")

    # Если совпадений нет, добавляем нового клиента
    cursor.execute(
        "INSERT INTO clients (first_name, phone_number, role) VALUES (%s, %s, %s)",
        (client.first_name, client.phone_number, client.role)
    )
    connection.commit()
    cursor.close()
    return {"message": "Клиент успешно создан"}

# Редактировать клиента по ID
@app.put("/clients/{id}")
def update_client(id: int, client_update: Client):
    cursor = connection.cursor()
    # Проверяем, существует ли клиент с указанным ID
    cursor.execute(f"SELECT * FROM clients WHERE id = {id}")
    existing_client = cursor.fetchone()

    if not existing_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    # Выполняем SQL-запрос для обновления данных клиента
    cursor.execute(
        "UPDATE clients SET first_name = %s, phone_number = %s, role = %s WHERE id = %s",
        (client_update.first_name, client_update.phone_number, client_update.role, id)
    )
    connection.commit()
    cursor.close()

    return {"message": "Клиент успешно обновлен"}
