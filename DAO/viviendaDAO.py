from Entities.vivienda import Vivienda
from db_conexion import coneccion_bd
from typing import List

class ViviendaDAO:

    def get_connection(self):
        
        conn = coneccion_bd()
        if conn is None:
            raise Exception("No se pudo conectar a la base de datos")
        return conn

    # INSERTAR VIVIENDA
    def insertVivienda(self, vivienda: Vivienda, userbd: str, passwbd: str) -> bool:
        sql = """
        INSERT INTO vivienda (
            nombre, balcony, bath_num, `condition`, floor, garage, garden, 
            ground_size, house_type, lift, loc_city, loc_district, loc_neigh, 
            m2_real, price, room_numbers, swimming_pool, terrace, unfurnished, usuario_id
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            vivienda.getNombre(), vivienda.getBalcony(), vivienda.getBathNum(),
            vivienda.getCondition(), vivienda.getFloor(), vivienda.getGarage(),
            vivienda.getGarden(), vivienda.getGroundSize(), vivienda.getHouseType(),
            vivienda.getLift(), vivienda.getLocCity(), vivienda.getLocDistrict(),
            vivienda.getLocNeigh(), vivienda.getM2Real(), vivienda.getPrice(),
            vivienda.getRoomNumbers(), vivienda.getSwimmingPool(), vivienda.getTerrace(),
            vivienda.getUnfurnished(), vivienda.getIdUsuario()
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            vivienda.setIdVivienda(cursor.lastrowid) 
            return cursor.rowcount == 1
        finally:
            cursor.close()
            conn.close()

    # SELECT TODAS
    def selectAllViviendas(self, user_id, userbd: str, passwbd: str) -> List[Vivienda]:
        sql = """
            SELECT id, nombre, balcony, bath_num, `condition`, floor, garage, garden, 
                ground_size, house_type, lift, loc_city, loc_district, loc_neigh, 
                m2_real, price, room_numbers, swimming_pool, terrace, unfurnished, usuario_id 
            FROM vivienda where usuario_id = %s
        """
        sql = sql % (user_id,)

        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            viviendas = []
            for row in results:
                v = Vivienda()
                v.setIdVivienda(row["id"]) 
                v.setNombre(row["nombre"])
                v.setBalcony(row["balcony"])
                v.setBathNum(row["bath_num"])
                v.setCondition(row["condition"])
                v.setFloor(row["floor"])
                v.setGarage(row["garage"])
                v.setGarden(row["garden"])
                v.setGroundSize(row["ground_size"])
                v.setHouseType(row["house_type"])
                v.setLift(row["lift"])
                v.setLocCity(row["loc_city"])
                v.setLocDistrict(row["loc_district"])
                v.setLocNeigh(row["loc_neigh"])
                v.setM2Real(row["m2_real"])
                v.setPrice(row["price"])
                v.setRoomNumbers(row["room_numbers"])
                v.setSwimmingPool(row["swimming_pool"])
                v.setTerrace(row["terrace"])
                v.setUnfurnished(row["unfurnished"])
                v.setIdUsuario(row["usuario_id"])
                viviendas.append(v)

            return viviendas

        finally:
            cursor.close()
            conn.close()

    # DELETE
    def deleteVivienda(self, vivienda: Vivienda, userbd: str, passwbd: str) -> bool:
        sql = "DELETE FROM vivienda WHERE id = %s"
        values = (vivienda.getIdVivienda(),)
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount == 1
        finally:
            cursor.close()
            conn.close()

    # SELECT BY ID
    def selectViviendaByID(self, vivienda: Vivienda, userbd: str, passwbd: str) -> Vivienda:
        idVivienda = vivienda.getIdVivienda()

        sql = "SELECT id FROM vivienda WHERE id = %s"
        values = (idVivienda,)

        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(sql, values)
            row = cursor.fetchone()

            if row:
                v = Vivienda()
                v.setIdVivienda(row['id'])
                return v
            else:
                return None
        finally:
            cursor.close()
            conn.close()