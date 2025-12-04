class Vivienda:
    def __init__(self, nombre, balcony, bath_num, condition, floor, garage, garden, ground_size, house_type, lift, loc_city, loc_district, loc_neigh, m2_real, price, room_numbers, swimming_pool, terrace, unfurnished, IdUsuario):
        self.id_vivienda = None
        self.nombre = nombre
        self.balcony = balcony
        self.bath_num = bath_num
        self.condition = condition
        self.floor = floor
        self.garage = garage
        self.garden = garden
        self.ground_size = ground_size
        self.house_type = house_type
        self.lift = lift
        self.loc_city = loc_city
        self.loc_district = loc_district
        self.loc_neigh = loc_neigh
        self.m2_real = m2_real
        self.price = price
        self.room_numbers = room_numbers
        self.swimming_pool = swimming_pool
        self.terrace = terrace
        self.unfurnished = unfurnished
        self.IdUsuario = IdUsuario

    def getIdVivienda(self):
        return self.id_vivienda
    def getNombre(self):
        return self.nombre
    def getBalcony(self):
        return self.baclcony
    def getBathNum(self):
        return self.bath_num
    def getCondition(self):
        return self.condition
    def getFloor(self):
        return self.floor
    def getGarage(self):
        return self.garage
    def getGarden(self):
        return self.garden
    def getGroundSize(self):
        return self.ground_size
    def getHouseType(self):
        return self.house_type
    def getLift(self):
        return self.lift
    def getLocCity(self):
        return self.loc_city
    def getLocDistrict(self):
        return self.loc_district
    def getLocNeigh(self):
        return self.loc_neigh
    def getM2Real(self):
        return self.m2_real
    def getPrice(self):
        return self.price
    def getRoomNumbers(self):
        return self.room_numbers
    def getSwimmingPool(self):
        return self.swimming_pool
    def getTerrace(self):
        return self.terrace
    def getUnfurnished(self):
        return self.unfurnished
    def getIdUsuario(self):
        return self.IdUsuario
    def setIdVivienda(self, nuevo_id_vivienda):
        self.id_vivienda = nuevo_id_vivienda
    def setNombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre
    def setPrice(self, nuevo_price):
        self.price = nuevo_price
    def setRoomNumbers(self, nuevo_room_numbers):
        self.room_numbers = nuevo_room_numbers
    def setM2Real(self, nuevo_m2_real):
        self.m2_real = nuevo_m2_real
    def setCondition(self, nueva_condition):
        self.condition = nueva_condition
    def setLocCity(self, nueva_loc_city):
        self.loc_city = nueva_loc_city
    def setLocDistrict(self, nueva_loc_district):
        self.loc_district = nueva_loc_district
    def setLocNeigh(self, nueva_loc_neigh):
        self.loc_neigh = nueva_loc_neigh
    def setGarage(self, nuevo_garage):
        self.garage = nuevo_garage
    def setGarden(self, nuevo_garden):
        self.garden = nuevo_garden
    def setSwimmingPool(self, nuevo_swimming_pool):
        self.swimming_pool = nuevo_swimming_pool
    def setTerrace(self, nuevo_terrace):
        self.terrace = nuevo_terrace
    def setBalcony(self, nuevo_baclcony):
        self.baclcony = nuevo_baclcony
    def setBathNum(self, nuevo_bath_num):
        self.bath_num = nuevo_bath_num
    def setFloor(self, nuevo_floor):
        self.floor = nuevo_floor
    def setGroundSize(self, nuevo_ground_size):
        self.ground_size = nuevo_ground_size
    def setHouseType(self, nuevo_house_type):
        self.house_type = nuevo_house_type
    def setLift(self, nuevo_lift):
        self.lift = nuevo_lift
    def setUnfurnished(self, nuevo_unfurnished):
        self.unfurnished = nuevo_unfurnished
    def setIdUsuario(self, nuevo_IdUsuario):
        self.IdUsuario = nuevo_IdUsuario

    def to_dict(self):
        """Convierte el objeto Vivienda a un diccionario para JSON."""
        return {
            "id_vivienda": self._id_vivienda,
            "nombre": self.nombre,
            "price": self.price,
            "m2_real": self.m2_real,
            "room_numbers": self.room_numbers,
            "bath_num": self.bath_num,
            "condition": self.condition,
            "house_type": self.house_type,
            "loc_city": self.loc_city,
            "loc_district": self.loc_district,
            "loc_neigh": self.loc_neigh,
            "balcony": self.balcony,
            "floor": self.floor,
            "garage": self.garage,
            "garden": self.garden,
            "ground_size": self.ground_size,
            "lift": self.lift,
            "swimming_pool": self.swimming_pool,
            "terrace": self.terrace,
            "unfurnished": self.unfurnished,
            "usuario_id": self.IdUsuario,
        }
    