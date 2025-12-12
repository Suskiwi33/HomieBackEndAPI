from flask import Flask, jsonify, request as req
import pandas as pd
from AI_Training.model_service import D_MAPPINGS, MAE, MODEL_FEATURES, MockRandomForestModel
from DAO.viviendaDAO import ViviendaDAO
from DAO.usuarioDAO import UsuarioDAO
from Entities.vivienda import Vivienda
from Entities.usuario import Usuario
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)

DAOV = ViviendaDAO()
DAOU = UsuarioDAO()

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})


app.config['JWT_SECRET_KEY'] = '123456'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


# LOGIN
@app.route("/api/login", methods=["POST"])
def login():
    data = req.get_json() or {}
    user = Usuario()
    user.setNombre(data.get("username"))
    user.setContraseña(data.get("password"))

    authenticated_user = DAOU.login(user)

    if authenticated_user:
        access_token = create_access_token(identity=authenticated_user.getNombre())
        return jsonify({
            "access_token": access_token,
            "user_id": authenticated_user.getId()
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


# REGISTER
@app.route("/api/register", methods=["POST"])
def register():
    data = req.get_json() or {}
    user = Usuario()
    user.setNombre(data.get("username"))
    user.setContraseña(data.get("password"))
    user.setEmail(data.get("email"))

    if DAOU.register(user):
        return jsonify({"message": f"Usuario '{user.getNombre()}' registrado correctamente."}), 201
    else:
        return jsonify({"error": "Error al registrar usuario"}), 500


# GET VIVIENDAS GUARDADAS
@app.route("/api/guardados/<int:userId>", methods=["GET"])
@jwt_required()
def get_guardados(userId):
    user_id = userId
    guardados = DAOV.selectAllViviendas(user_id) or []
    guardados_list = [v.to_dict() for v in guardados]

    return jsonify({"usuario": user_id, "guardados": guardados_list})


# INSERTAR VIVIENDA
@app.route("/api/addVivienda", methods=["POST"])
@jwt_required()
def insertVivienda():
    data = req.get_json(force=True) or {}

    campos_esperados = [
        "nombre", "balcony", "bath_num", "condition", "floor", "garage", "garden",
        "ground_size", "house_type", "lift", "loc_city", "loc_district", "loc_neigh",
        "m2_real", "price", "room_num", "swimming_pool", "terrace", "unfurnished",
        "user_id"
    ]

    datos = {campo: data.get(campo) for campo in campos_esperados}

    if not datos.get("nombre") or datos.get("price") is None:
        return jsonify({"error": "Los campos 'nombre' y 'price' son obligatorios"}), 400

    try:
        for n in ["price", "m2_real"]:
            if datos.get(n) is not None:
                datos[n] = float(datos[n])

        for n in ["room_num", "bath_num", "floor"]:
            if datos.get(n) is not None:
                datos[n] = int(datos[n])

        for b in ["balcony", "garage", "garden", "lift", "swimming_pool", "terrace", "unfurnished"]:
            if datos.get(b) is not None:
                datos[b] = int(datos[b])

    except ValueError:
        return jsonify({"error": "Datos numéricos inválidos"}), 400

    try:
        v = Vivienda()
        v.setNombre(datos["nombre"])
        v.setBalcony(datos.get("balcony", 0))
        v.setBathNum(datos.get("bath_num", 0))
        v.setCondition(datos.get("condition", ""))
        v.setFloor(datos.get("floor", 0))
        v.setGarage(datos.get("garage", 0))
        v.setGarden(datos.get("garden", 0))
        v.setGroundSize(datos.get("ground_size", 0))
        v.setHouseType(datos.get("house_type", ""))
        v.setLift(datos.get("lift", 0))
        v.setLocCity(datos.get("loc_city", ""))
        v.setLocDistrict(datos.get("loc_district", ""))
        v.setLocNeigh(datos.get("loc_neigh", ""))
        v.setM2Real(datos.get("m2_real", 0))
        v.setRoomNumbers(datos.get("room_num", 0))
        v.setSwimmingPool(datos.get("swimming_pool", 0))
        v.setTerrace(datos.get("terrace", 0))
        v.setUnfurnished(datos.get("unfurnished", 0))
        v.setPrice(datos["price"])
        v.setIdUsuario(datos["user_id"])
    except Exception as e:
        return jsonify({"error": f"Error al crear Vivienda: {str(e)}"}), 500

    ok = DAOV.insertVivienda(v)

    if not ok:
        return jsonify({"error": "Error al insertar vivienda"}), 500

    return jsonify({"message": "Vivienda insertada", "id": v.getIdVivienda()}), 201


# DELETE VIVIENDA
@app.route("/api/deleteVivienda/<int:id>", methods=["DELETE"])
@jwt_required()
def deleteVivienda(id):

    try:
        idv = int(id)
    except ValueError:
        return jsonify({"error": "Id inválido"}), 400

    temp = Vivienda()
    temp.setIdVivienda(idv) 

    viv = DAOV.selectViviendaByID(temp)

    if not viv:
        return jsonify({"error": "Vivienda no encontrada"}), 404

    ok = DAOV.deleteVivienda(viv)

    if not ok:
        return jsonify({"error": "Error eliminando vivienda"}), 500

    return jsonify({"message": "Vivienda eliminada"}), 200


# PREDICT PRICE
@app.route("/api/predictPrice", methods=["POST"])
def predictPrice():
    data = req.get_json() or {}

    try:
        input_data = {}
        for feature in MODEL_FEATURES:
            if feature in D_MAPPINGS:
                input_data[feature] = data.get(feature, "")
            else:
                input_data[feature] = data.get(feature, 0)

        df_usuario = pd.DataFrame([input_data])

        for col, mapping in D_MAPPINGS.items():
            if col in df_usuario:
                df_usuario[col] = df_usuario[col].map(mapping)

        df_pred = pd.DataFrame(0, index=[0], columns=MODEL_FEATURES)

        for col in df_usuario.columns:
            if col in df_pred.columns:
                df_pred[col] = df_usuario[col].iloc[0]

        df_pred = df_pred.fillna(0).astype(float)

        modelo = MockRandomForestModel()
        raw = modelo.predict(df_pred)

        try:
            precio_base = float(raw[0])
        except:
            precio_base = float(raw)

        precio_final = precio_base + MAE

        return jsonify({
            "predicted_price": round(precio_final, 2),
            "currency": "EUR"
        })

    except Exception as e:
        print("ERROR predictPrice:", e)
        return jsonify({"error": str(e)}), 500


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)