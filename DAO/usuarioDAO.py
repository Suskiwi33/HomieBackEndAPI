from Entities.usuario import Usuario
from db_conexion import coneccion_bd

class UsuarioDAO:

    def get_connection(self, user, passw):
        conn = coneccion_bd(user, passw)
        conn = coneccion_bd()
        if conn is None:
            raise Exception("No se pudo conectar a la base de datos")
        return conn
    
    # LOGIN
    def login(self, user, userbd, passwbd):
        sql = "SELECT id, usuario, password FROM usuario WHERE usuario = %s AND password = %s"
        values = (user.getNombre(), user.getContraseña())
        conn = self.get_connection(userbd, passwbd)
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            result = cursor.fetchone()
            if result:
                user.setId(result[0])
                return user
            else:
                return None
        finally:
            cursor.close()
            conn.close()

    # REGISTRO
    def register(self, user: Usuario, userbd, passwbd):
        sql = "INSERT INTO usuario (usuario, password, email) VALUES (%s, %s, %s)"
        values = (user.getNombre(), user.getContraseña(), user.getEmail())
        conn = self.get_connection(userbd, passwbd)
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount == 1
        finally:
            cursor.close()
            conn.close()