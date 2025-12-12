import mysql.connector

def coneccion_bd():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="homie"
        )
        if connection.is_connected():
            print("✅ Conexión establecida con la base de datos.")
            return connection
    except mysql.connector.Error as err:
        print(f"❌ Error al conectar con MySQL: {err}")
        return None