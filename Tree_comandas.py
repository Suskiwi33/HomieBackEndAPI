import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np


try:
  
    df = pd.read_csv("Docs/houses_barcelona.csv") 
except FileNotFoundError:
    print("Error: Asegúrate de que el archivo 'houses_barcelona.csv' exista y la ruta sea correcta.")
    exit()

df.dropna(subset=['price'], inplace=True)
y = df['price'] 

columnas_caracteristicas = [
    "balcony", "bath_num", "condition", "floor", "garage", "garden", 
    "ground_size", "house_type", "lift", "loc_city", "loc_district", "loc_neigh", 
    "m2_real", "swimming_pool","room_numbers", "terrace", "unfurnished"
]

X = df[columnas_caracteristicas].copy() 
d_condition = {'promoción de obra nueva': 0, 'segunda mano/a reformar': 1, 'segunda mano/buen estado': 2, 'segunda mano/reformado': 3}
X['condition'] = X['condition'].map(d_condition)

d_garage = {'no indicado': 0, 'plaza de garaje incluida en el precio': 1, 'plaza de garaje por 10.000 eur adicionales': 2, 'plaza de garaje por 12.000 eur adicionales': 3, 'plaza de garaje por 5.000 eur adicionales': 4, 'plaza de garaje por 6.000 eur adicionales': 5, 'plaza de garaje por 8.000 eur adicionales': 6}
X['garage'] = X['garage'].map(d_garage)

d_house_type = {'Apartamento': 0, 'Casa o chalet independiente': 1, 'Casa o chalet adosado': 2, 'Estudio': 3, 'Finca rústica': 4, 'Piso': 5}
X['house_type'] = X['house_type'].map(d_house_type)

d_loc_city = {'Barcelona': 0, 'Hospitalet de Llobregat': 1, 'Vilafranca del Penedès': 2}
X['loc_city'] = X['loc_city'].map(d_loc_city)

d_loc_district = {'Distrito Centre Vila': 0, 'Distrito Eixample': 1, 'Distrito La Escorxador': 2, 'Distrito Sant Julià': 3, 'Distrito Sant Pere': 4, 'Distrito Sants-Badal': 5}
X['loc_district'] = X['loc_district'].map(d_loc_district)

d_loc_neigh = {'La Barceloneta': 0, 'La Florida': 1, 'Les Corts': 2, 'Llefia': 3, 'Navas': 4, 'Sant Marti': 5, 'Sant Pere': 6, 'Sant Julià': 7, 'Sants-Badal': 8, 'Vilafranca del Penedès': 9}
X['loc_neigh'] = X['loc_neigh'].map(d_loc_neigh)


columnas_categoricas = X.select_dtypes(include=['object']).columns
X_procesado = pd.get_dummies(X, columns=columnas_categoricas, dummy_na=False)

X_final = X_procesado.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42
)
 
print("Entrenando el modelo de Bosque Aleatorio...")
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
modelo_rf.fit(X_train, y_train)

print("Entrenamiento completado.")

predictions = modelo_rf.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

print(f"\n--- Resultado de la Evaluación ---")
print(f"Error Absoluto Medio (MAE): {mae:,.2f} [Moneda]")
print(f"En promedio, la predicción se desvía del precio real por {mae:,.2f} unidades.")

def predecir_precio_casa_interactivo(modelo, caracteristicas_modelo, mapeos):
    """
    Recoge datos de la casa por línea de comandos y predice el precio.
    """
    print("\n" + "="*50)
    print("🏠 INGRESE LOS DETALLES DE LA CASA PARA LA PREDICCIÓN 🏠")
    print("="*50)

    datos_usuario = {}
    
    print("\nPor favor, introduzca los siguientes datos:")
    
    try:
        datos_usuario['m2_real'] = float(input("Superficie útil (m2_real): "))
        datos_usuario['room_numbers'] = int(input("Número de habitaciones (room_numbers): "))
        datos_usuario['bath_num'] = int(input("Número de baños (bath_num): "))
        datos_usuario['floor'] = int(input("Piso (floor, 0 para planta baja): "))
        datos_usuario['ground_size'] = float(input("Tamaño del terreno (ground_size, 0 si no aplica): "))
    except ValueError:
        print("ERROR: Superficie, habitaciones, baños, piso o terreno deben ser números. Terminando...")
        return
    
    datos_usuario['balcony'] = 1 if input("¿Tiene balcón? (s/n): ").lower() == 's' else 0
    datos_usuario['garden'] = 1 if input("¿Tiene jardín? (s/n): ").lower() == 's' else 0
    datos_usuario['lift'] = 1 if input("¿Tiene ascensor? (s/n): ").lower() == 's' else 0
    datos_usuario['swimming_pool'] = 1 if input("¿Tiene piscina? (s/n): ").lower() == 's' else 0
    datos_usuario['terrace'] = 1 if input("¿Tiene terraza? (s/n): ").lower() == 's' else 0
    datos_usuario['unfurnished'] = 1 if input("¿Está sin amueblar (unfurnished)? (s/n): ").lower() == 's' else 0

    
    print("\n--- Estado (condition) ---")
    for k, v in mapeos['condition'].items():
        print(f"[{v}] {k}")
    cond_input = int(input(f"Seleccione el número de estado: "))
    datos_usuario['condition'] = cond_input
    
    
    print("\n--- Garaje (garage) ---")
    for k, v in mapeos['garage'].items():
        print(f"[{v}] {k}")
    garage_input = int(input(f"Seleccione el número de garaje: "))
    datos_usuario['garage'] = garage_input
    
    
    print("\n--- Tipo de casa (house_type) ---")
    for k, v in mapeos['house_type'].items():
        print(f"[{v}] {k}")
    house_type_input = int(input(f"Seleccione el número de tipo de casa: "))
    datos_usuario['house_type'] = house_type_input

    print("\n--- Ciudad (loc_city) ---")
    for k, v in mapeos['loc_city'].items():
        print(f"[{v}] {k}")
    city_input = int(input(f"Seleccione el número de ciudad: "))
    datos_usuario['loc_city'] = city_input

    print("\n--- Distrito (loc_district) ---")
    for k, v in mapeos['loc_district'].items():
        print(f"[{v}] {k}")
    district_input = int(input(f"Seleccione el número de distrito: "))
    datos_usuario['loc_district'] = district_input
    
    
    print("\n--- Barrio (loc_neigh) ---")
    for k, v in mapeos['loc_neigh'].items():
        print(f"[{v}] {k}")
    neigh_input = int(input(f"Seleccione el número de barrio: "))
    datos_usuario['loc_neigh'] = neigh_input


    df_usuario = pd.DataFrame([datos_usuario])

    df_prediccion = pd.DataFrame(0, index=[0], columns=caracteristicas_modelo)

    for col in df_usuario.columns:
        if col in df_prediccion.columns:
            df_prediccion[col] = df_usuario[col].iloc[0]

    precio_predicho = modelo.predict(df_prediccion)
    
    print("\n" + "="*50)
    print(f"⭐ PRECIO PREDICHO DEL MODELO ⭐")
    print(f"El precio estimado es: **{precio_predicho[0]:,.2f} €**")
    print(f"Basado en un Error Absoluto Medio (MAE) de {mae:,.2f}.")
    print("="*50)


mapeos_disponibles = {
    'condition': {v: k for k, v in d_condition.items()}, # Invertimos el mapeo para mostrar opciones
    'garage': {v: k for k, v in d_garage.items()},
    'house_type': {v: k for k, v in d_house_type.items()},
    'loc_city': {v: k for k, v in d_loc_city.items()},
    'loc_district': {v: k for k, v in d_loc_district.items()},
    'loc_neigh': {v: k for k, v in d_loc_neigh.items()},
}

predecir_precio_casa_interactivo(modelo_rf, X_final.columns, mapeos_disponibles)