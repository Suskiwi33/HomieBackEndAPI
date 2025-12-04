from vivienda import Vivienda
from usuario import Usuario
from db_conexion import coneccion_bd
from typing import List, Tuple

class ViviendaDAO:
    def __init__(self):
        self.__db = None
        self._user = None
        self._password = None
    
    def conectarBaseDatos(self):
        """Connect to the database using provided credentials."""
        dbconnector = coneccion_bd()
        self.__db = dbconnector
        if self.__db is not None:
            return True
        else:
            return False
        
    # EN EL ARCHIVO VIVIENDA_DAO.PY (o donde esté el método login)

    def login(self, user):
        """
        Verifica las credenciales del usuario de la aplicación usando
        la conexión de servicio (self.__db).
        """
        self.ensure_connection() # Asegura que self.__db está activo (usando credenciales de servicio)

        self._user = user.getNombre()
        self._password = user.getContraseña()

        sql = "SELECT id, usuario, password FROM usuario WHERE usuario = %s AND password = %s"
        values = (self._user, self._password)

        try:
            # Usa el objeto de conexión ALMACENADO (self.__db), no la función coneccion_bd
            with self.__db.cursor() as cursor: 
                
                # 1. Ejecutar la consulta con parámetros
                cursor.execute(sql, values)
                
                # 2. Verificar el resultado
                result = cursor.fetchone() 
                
                if result:
                    print(f"✅ User {self._user} logged in successfully.")
                    # Opcional: Podrías guardar el ID del usuario: user.setIdUsuario(result[0])
                    return True
                else:
                    print(f"❌ Login failed for user {self._user}.")
                    return False
                    
        except Exception as e:
            print(f"Database error during login: {e}")
            # En caso de error de BD, el login falla
            return False

    def register(self, user: Usuario):
        self.ensure_connection()
        with self.__db.cursor() as dbCursor:
            sql = "INSERT INTO usuario (usuario, password) VALUES (%s, %s)"
            values = (user.getNombre(), user.getContraseña())
            dbCursor.execute(sql, values)
            self.__db.commit()
            return self.checkRows(dbCursor.rowcount)

    def insertVivienda(self, vivienda: Vivienda):
        self.ensure_connection()
        with self.__db.cursor() as dbCursor:
            sql =  """
        INSERT INTO vivienda (
        nombre, balcony, bath_num, `condition`, floor, garage, garden, 
        ground_size, house_type, lift, loc_city, loc_district, loc_neigh, 
        m2_real, price, room_numbers, swimming_pool, terrace, unfurnished, usuario_id
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            vivienda.getNombre(),
            vivienda.getBalcony(),
            vivienda.getBathNum(),
            vivienda.getCondition(),
            vivienda.getFloor(),
            vivienda.getGarage(),
            vivienda.getGarden(),
            vivienda.getGroundSize(),
            vivienda.getHouseType(),
            vivienda.getLift(),
            vivienda.getLocCity(),
            vivienda.getLocDistrict(),
            vivienda.getLocNeigh(),
            vivienda.getM2Real(),
            vivienda.getPrice(),
            vivienda.getRoomNumbers(),
            vivienda.getSwimmingPool(),
            vivienda.getTerrace(),
            vivienda.getUnfurnished(),
            vivienda.getIdUsuario()
        )
        dbCursor.execute(sql, values)
        self.db.commit()

    def selectAllViviendas(self) -> List[Vivienda]:
            self.ensure_connection()
            viviendaARR: List[Vivienda] = []

            with self.__db.cursor(dictionary=True) as dbCursor:
                sql = """SELECT nombre, balcony, bath_num, condition, floor, garage, garden, 
                ground_size, house_type, lift, loc_city, loc_district, loc_neigh, 
                m2_real, price, room_numbers, swimming_pool, terrace, unfurnished, usuario_id FROM vivienda"""
                dbCursor.execute(sql)
                tuplaViviendas = dbCursor.fetchall()

                if not tuplaViviendas:
                    print("No hay viviendas en la base de datos (consulta vacía).")
                    return []

                for tupla in tuplaViviendas:
                    vivienda = Vivienda()
                    vivienda.setNombre(tupla["nombre"])
                    vivienda.setBalcony(tupla["balcony"])
                    vivienda.setBathNum(tupla["bath_num"])
                    vivienda.setCondition(tupla["condition"])
                    vivienda.setFloor(tupla["floor"])
                    vivienda.setGarage(tupla["garage"])
                    vivienda.setGarden(tupla["garden"])
                    vivienda.setGroundSize(tupla["ground_size"])
                    vivienda.setHouseType(tupla["house_type"])
                    vivienda.setLift(tupla["lift"])
                    vivienda.setLocCity(tupla["loc_city"])
                    vivienda.setLocDistrict(tupla["loc_district"])
                    vivienda.setLocNeigh(tupla["loc_neigh"])
                    vivienda.setM2Real(tupla["m2_real"])
                    vivienda.setPrice(tupla["price"])
                    vivienda.setRoomNumbers(tupla["room_numbers"])
                    vivienda.setSwimmingPool(tupla["swimming_pool"])
                    vivienda.setTerrace(tupla["terrace"])
                    vivienda.setUnfurnished(tupla["unfurnished"])
                    vivienda.setIdUsuario(tupla["usuario_id"])
                    viviendaARR.append(vivienda)

            return viviendaARR
        
    def deleteVivienda(self, vivienda: Vivienda):
            self.ensure_connection()
            with self.__db.cursor() as dbCursor:
                sql = "DELETE FROM vivienda WHERE idVivienda = %s"
                values = (vivienda.getId(),)
                dbCursor.execute(sql, values)
                self.db.commit()
                return self.checkRows(dbCursor.rowcount)

    def selectViviendaByID(self, vivienda_template):
            """Busca una vivienda por ID."""
            for v in self.viviendas:
                if v.getIdVivienda() == vivienda_template.getIdVivienda():
                    return v
            return None

    def closeConnection(self):
            """Simula el cierre de la conexión (no hace nada en la versión en memoria)."""
            print("DEBUG: Conexión de DAO cerrada (simulada).")
            pass
    
    def ensure_connection(self):
        """Asegura que la conexión a la BD (self.__db) está activa, reconectando si es necesario."""
        # Se reconecta si la conexión no existe o está cerrada
        if self.__db is None or not self.__db.is_connected():
            print("DEBUG: Intentando reconectar a la base de datos...")
            
            # Llama a la función de conexión con las credenciales de servicio (fijas)
            new_db = coneccion_bd() 
            
            if new_db is None:
                # Si la reconexión falla, lanza una excepción que Flask atrapará como un 500
                raise Exception("ERROR FATAL: No se pudo establecer la conexión a la base de datos de servicio.")
            
            self.__db = new_db
        # Si ya está conectada, no hace nada.