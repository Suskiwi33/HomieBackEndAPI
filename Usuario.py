class Usuario:
    def __init__(self, nombre_usuario="", contraseña="", email=""):
        self.id_usuario = None
        self.nombre = nombre_usuario
        self.contraseña = contraseña
        self.email = email
    
    def setId(self, id):
        self.id_usuario = id

    def getId(self):
        return self.id_usuario

    def getIdUsuario(self):
        return self.id_usuario
    
    def getNombre(self):
        return self.nombre
    
    def getContraseña(self):
        return self.contraseña
    
    def getEmail(self):
        return self.email
    
    def setNombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre  

    def setContraseña(self, nueva_contraseña):
        self.contraseña = nueva_contraseña
    
    def setEmail(self, nuevo_email):
        self.email = nuevo_email