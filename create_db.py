import mysql.connector

host = 'localhost'
database = 'user_token'
user = 'root'
password = ''
port = 3306

credentials_db = mysql.connector.connect(
    user=user,
    password=password,
    database=database,
    host=host
)
cursor = credentials_db.cursor()

# cursor.execute("CREATE DATABASE user_token")
# cursor.execute("CREATE TABLE user_credentials (user_id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(255), token VARCHAR(255))")

credentials_db.commit()
cursor.close()
credentials_db.close()