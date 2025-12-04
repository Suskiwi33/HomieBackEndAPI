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
        
    def login(self, user):
        self._user = user.getNombre()
        self._password = user.getContraseña()
        
        # NOTE: Using string formatting for SQL is dangerous (SQL Injection). 
        # Always use parameterization as shown with %s.
        sql = "SELECT * FROM usuario WHERE nombre = %s AND contraseña = %s"
        values = (self._user, self._password)

        # --- Database interaction is needed here ---
        
        # 1. Get a database cursor (self._db_connection is an assumption)
        cursor = coneccion_bd.cursor()
        
        # 2. Execute the query
        cursor.execute(sql, values)
        
        # 3. Fetch one result (or check how many rows were affected/returned)
        result = cursor.fetchone() 
        
        # 4. Check the result
        # If fetchone() returns a row (i.e., not None), the user exists.

        # --- Hypothetical implementation using standard DB-API conventions ---

        try:
            # Assuming 'self._connection' is your active database connection
            with self._connection.cursor() as cursor:
                # Execute the query with parameterized values
                cursor.execute(sql, values)
                
                # Try to fetch one result. If a row is found, it means the user exists.
                # result will be a tuple/dict (the row) if found, or None if not found.
                result = cursor.fetchone() 
                
                # If result is NOT None (i.e., a row was found), return True
                if result:
                    print(f"User {self._user} logged in successfully.")
                    return True
                else:
                    # If no row was found, return False
                    print(f"Login failed for user {self._user}.")
                    return False
                    
        except Exception as e:
            # Handle database connection or execution errors
            print(f"Database error during login: {e}")
            return False # Return False on error
        
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