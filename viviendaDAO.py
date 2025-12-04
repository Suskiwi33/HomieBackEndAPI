from vivienda import Vivienda
from usuario import Usuario
from db_conexion import coneccion_bd
from typing import List, Tuple

class ViviendaDAO:
    def __init__(self):
        self.__db = None
        self._user = None
        self._password = None
        
    def login(self, user):
        """Connect to the database and store credentials for reconnection."""
        self._user = user.getNombre()
        self._password = user.getContraseña()
        dbconnector = coneccion_bd(self._user, self._password)
        self.__db = dbconnector
        if self.__db is not None:
            return True
        else:
            return False
        
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
                vivienda.setBath_num(tupla["bath_num"])
                vivienda.setCondition(tupla["condition"])
                vivienda.setFloor(tupla["floor"])
                vivienda.setGarage(tupla["garage"])
                vivienda.setGarden(tupla["garden"])
                vivienda.setGround_size(tupla["ground_size"])
                vivienda.setHouse_type(tupla["house_type"])
                vivienda.setLift(tupla["lift"])
                vivienda.setLoc_city(tupla["loc_city"])
                vivienda.setLoc_district(tupla["loc_district"])
                vivienda.setLoc_neigh(tupla["loc_neigh"])
                vivienda.setM2_real(tupla["m2_real"])
                vivienda.setPrice(tupla["price"])
                vivienda.setRoom_numbers(tupla["room_numbers"])
                vivienda.setSwimming_pool(tupla["swimming_pool"])
                vivienda.setTerrace(tupla["terrace"])
                vivienda.setUnfurnished(tupla["unfurnished"])
                vivienda.setUsuario_id(tupla["usuario_id"])
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