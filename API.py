from flask import Flask, jsonify, request as req
import pandas as pd
from model_service import D_MAPPINGS, MAE, MODEL_FEATURES, MockRandomForestModel
from viviendaDAO import ViviendaDAO
from vivienda import Vivienda
from usuario import Usuario
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
DAO = ViviendaDAO()

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

# JWT 
app.config['JWT_SECRET_KEY'] = '123456'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

@app.route("/api/login", methods=["POST"])
def login():
    """Ruta para simular el inicio de sesión de un usuario y devolver su ID."""
    data = req.get_json() or {}
    
    # 1. Crear y cargar el objeto Usuario con las credenciales
    user = Usuario()
    user.setNombre(data.get("username"))
    user.setContraseña(data.get("password"))
    
    # 2. Llamar al DAO. Si el login es exitoso, 'authenticated_user' será el objeto Usuario
    #    que ya tiene el ID cargado internamente por el método DAO.login.
    authenticated_user = DAO.login(user) # Asumiendo que DAO es una instancia de tu clase DAO
    
    if authenticated_user:
        # 3. Obtener el ID y el nombre del usuario autenticado
        user_id = authenticated_user.getIdUsuario() 
        username = authenticated_user.getNombre()
        
        # 4. Crear el token (la identidad puede ser el ID o el nombre)
        access_token = create_access_token(identity=username) 
        
        # 5. Devolver el token Y el ID del usuario
        return jsonify({
            "access_token": access_token,
            "user_id": user_id 
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401
    

@app.route("/api/register", methods=["POST"])
def register():
    """Ruta para registrar un nuevo usuario."""
    data = req.get_json() or {}
    user = Usuario()
    user.setNombre(data.get("username"))
    user.setContraseña(data.get("password"))
    user.setEmail(data.get("email"))
    
    if DAO.register(user):
        return jsonify({"message": f"Usuario '{user.getNombre()}' registrado correctamente."}), 201
    else:
        return jsonify({"error": "Error al registrar el usuario."}), 500

@app.route("/api/guardados", methods=["GET"])
@jwt_required()
def get_guardados():
    usuario_nombre = get_jwt_identity()
    guardados = DAO.selectViviendasByUsuario(usuario_nombre) or []
    guardados_list = [v.to_dict() for v in guardados]
    return jsonify({"usuario": usuario_nombre, "guardados": guardados_list})

@app.route("/api/addVivienda", methods=["POST"])
def insertVivienda():
    """Ruta para insertar una nueva vivienda en la base de datos simulada."""
    data = req.get_json() or {}

    campos_esperados = [
        "nombre", "balcony", "bath_num", "condition", "floor", "garage", "garden",
        "ground_size", "house_type", "lift", "loc_city", "loc_district", "loc_neigh",
        "m2_real", "price", "room_num", "swimming_pool", "terrace", "unfurnished", 
        "user_id"
    ]

    datos_vivienda = {campo: data.get(campo) for campo in campos_esperados}

    if not datos_vivienda.get("nombre") or datos_vivienda.get("price") is None:
        return jsonify({"error": "Los campos 'nombre' y 'price' son obligatorios"}), 400

    try:
        if datos_vivienda.get("price") is not None:
            datos_vivienda["price"] = float(datos_vivienda["price"])
        if datos_vivienda.get("m2_real") is not None:
            datos_vivienda["m2_real"] = float(datos_vivienda["m2_real"])
        if datos_vivienda.get("room_num") is not None:
            datos_vivienda["room_num"] = int(datos_vivienda["room_num"])
        if datos_vivienda.get("bath_num") is not None:
            datos_vivienda["bath_num"] = int(datos_vivienda["bath_num"])
        if datos_vivienda.get("floor") is not None:
            datos_vivienda["floor"] = int(datos_vivienda["floor"])
        for key in ["balcony", "garage", "garden", "lift", "swimming_pool", "terrace", "unfurnished"]:
            if datos_vivienda.get(key) is not None:
                 datos_vivienda[key] = int(datos_vivienda[key])
            
    except ValueError:
        return jsonify({"error": "Uno o más campos numéricos ('price', 'm2_real', etc.) no son válidos"}), 400
        
    try:
        v = Vivienda()
        v.setNombre(datos_vivienda["nombre"])
        v.setBalcony(datos_vivienda.get("balcony", 0))
        v.setBathNum(datos_vivienda.get("bath_num", 0))
        v.setCondition(datos_vivienda.get("condition", ""))
        v.setFloor(datos_vivienda.get("floor", 0))
        v.setGarage(datos_vivienda.get("garage", 0))
        v.setGarden(datos_vivienda.get("garden", 0))
        v.setGroundSize(datos_vivienda.get("ground_size", 0.0))
        v.setHouseType(datos_vivienda.get("house_type", ""))
        v.setLift(datos_vivienda.get("lift", 0))
        v.setLocCity(datos_vivienda.get("loc_city", ""))
        v.setLocDistrict(datos_vivienda.get("loc_district", ""))
        v.setLocNeigh(datos_vivienda.get("loc_neigh", ""))
        v.setM2Real(datos_vivienda.get("m2_real", 0.0))
        v.setRoomNumbers(datos_vivienda.get("room_num", 0))
        v.setSwimmingPool(datos_vivienda.get("swimming_pool", 0))
        v.setTerrace(datos_vivienda.get("terrace", 0))
        v.setUnfurnished(datos_vivienda.get("unfurnished", 0))
        v.setPrice(datos_vivienda["price"])
        v.setIdUsuario(datos_vivienda["user_id"])
        
    except Exception as e:
        return jsonify({"error": f"Error al inicializar la Vivienda: {str(e)}"}), 500

    ok = DAO.insertVivienda(v)
    
    if not ok:
        return jsonify({"error": "Error al insertar la vivienda en la base de datos simulada"}), 500
        
    return jsonify({"message": f"Vivienda '{v.getNombre()}' insertada correctamente", "id": v.getIdVivienda()}), 201


@app.route("/api/deleteVivienda", methods=["DELETE"]) # Ruta corregida
def deleteVivienda():
    """Ruta para eliminar una vivienda por su ID."""
    
    id_str = req.args.get("id")
    if not id_str:
        return jsonify({"error": "id de Vivienda requerido"}), 400
    try:
        idv = int(id_str)
    except ValueError:
        return jsonify({"error": "id debe ser un número entero"}), 400

    
    vivienda_temp = Vivienda()
    vivienda_temp.setIdVivienda(idv)
    
    existing_vivienda = DAO.selectViviendaByID(vivienda_temp)
    

    if not existing_vivienda:
        return jsonify({"error": f"Vivienda con ID {idv} no encontrada"}), 404

    
    ok = DAO.deleteVivienda(existing_vivienda)
    
    
    if not ok:
        return jsonify({"error": "Error al eliminar la vivienda en la base de datos simulada"}), 500
        
    return jsonify({"message": f"Vivienda con ID {idv} y nombre '{existing_vivienda.getNombre()}' eliminada correctamente"})


@app.route("/api/predictPrice", methods=["POST", "OPTIONS"])
def predictPrice():
    if req.method == "OPTIONS":
        return "", 200
    
    """
    Endpoint para predecir el precio de una vivienda usando el modelo RF.
    Acepta un JSON con todas las características de la vivienda.
    """
    data = req.get_json() or {}

    try:
        
        input_data = {}
        for feature in MODEL_FEATURES:
            # Si la columna está en los datos de entrada, la usa. Si no, usa 0 o '' dependiendo del tipo (simulación)
            if feature in D_MAPPINGS: # Es una columna categórica
                 # Si la categoría no se proporciona, usa una cadena vacía que se mapeará a NaN
                 input_data[feature] = data.get(feature, '') 
            else: # Es una columna numérica
                 input_data[feature] = data.get(feature, 0) # Usa 0 como default
        
        df_usuario = pd.DataFrame([input_data])

        # 2. Aplicar los mapeos de categorías (condition, house_type, etc.)
        for col, mapping in D_MAPPINGS.items():
            if col in df_usuario.columns:
                # El mapeo convierte las cadenas a números. Las cadenas no mapeadas se convierten a NaN.
                df_usuario[col] = df_usuario[col].map(mapping)
        
        # 3. Alineación de columnas: crea un DataFrame vacío con la estructura exacta
        #    del modelo y rellena los valores del usuario. Esto maneja automáticamente
        #    las columnas que faltan (se quedan a 0) y el orden.
        df_prediccion = pd.DataFrame(0, index=[0], columns=MODEL_FEATURES)

        # Copia los valores del usuario a las columnas correspondientes
        for col in df_usuario.columns:
            if col in df_prediccion.columns:
                # Usamos .iloc[0] para asegurar que se copia el valor y no la Serie completa
                df_prediccion[col] = df_usuario[col].iloc[0] 
        
        # 4. Asegurarse de que los tipos de datos son correctos.
        #    Se maneja automáticamente si MODEL_FEATURES es de tipo Index, pero lo forzamos.
        df_prediccion = df_prediccion.fillna(0) # Rellenar NaNs (de mapeos fallidos) con 0
        df_prediccion = df_prediccion.astype(float) # Forzar todos los tipos a float para el modelo

        # 5. Predicción
        modelo_rf = MockRandomForestModel()
        raw_prediction = modelo_rf.predict(df_prediccion)
        
        # --- BLOQUE A PRUEBA DE BALAS ---
        # Detectamos automáticamente si viene como lista o como número
        try:
            # Intentamos acceder como si fuera lista/array (ej: [250000])
            precio_base = float(raw_prediction[0])
        except (TypeError, IndexError):
            # Si falla (porque ya es un número), lo usamos directamente
            precio_base = float(raw_prediction)
        # -------------------------------

        precio_final = precio_base + MAE
        
        return jsonify({
            "predicted_price": round(precio_final, 2),
            "currency": "EUR"
        })

    except Exception as e:
        print(f"ERROR en predictPrice: {str(e)}")
        return jsonify({"error": f"Error interno al procesar la predicción: {str(e)}"}), 500

@app.teardown_appcontext
def close_db_connection(exception):
    """Cierra la conexión de la base de datos al finalizar la solicitud (simulado)."""
    DAO.closeConnection()


if __name__ == '__main__':
    # Ejecuta la aplicación Flask
    # NOTA: Para probar las rutas de la API, inicia la aplicación y usa un cliente (como cURL o Postman)
    print("\n==============================================")
    print("Flask App Iniciada.")
    print("Prueba las rutas POST y GET para interactuar con la API simulada.")
    print("==============================================")

    app.run(debug=True, host='0.0.0.0', port=5000)