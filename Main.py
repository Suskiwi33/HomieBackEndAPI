import db_conexion

user = "root"
password = "123456"


conexion = db_conexion.coneccion_bd(user, password)
if conexion:
    print("Conexión exitosa a la base de datos.")
    conexion.close()
