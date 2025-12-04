import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np
import os

# --- 1. Definición de Mapeos para Madrid (Simplificados) ---

# Mapeo 'condition'
d_condition = {
    'promoción de obra nueva': 0, 
    'segunda mano/para reformar': 1, 
    'segunda mano/buen estado': 2,
    'segunda mano/reformado': 3,
    'condition': 99 # Inválido
}

# Función para mapear 'garage' de forma simplificada
def map_garage(val):
    """
    Convierte los múltiples valores de garaje a 0 (No/Inválido), 1 (Incluido), 2 (Costo adicional).
    """
    if pd.isna(val) or val == 'garage':
        return 0
    if val == 'plaza de garaje incluida en el precio':
        return 1
    # Si contiene "adicionales", lo mapeamos a 2
    if isinstance(val, str) and 'adicionales' in val:
        return 2
    return 0 

# Mapeo 'house_type'
d_house_type = {
    'Piso': 0, 
    ' Chalet adosado': 1, 
    ' Chalet pareado': 2, 
    'Dúplex': 3, 
    ' Casa o chalet independiente': 4, 
    'Ático': 5, 
    ' Casa o chalet': 6, 
    'Estudio': 7, 
    ' Finca rústica': 8,
    'house_type': 99 # Inválido
}

# Mapeo 'loc_city'
d_loc_city = {
    'Madrid': 0, 
    'Pinto': 1,
    'loc_city': 99 # Inválido
}

# Mapeo 'loc_district' (Top 6 distritos y el resto a 6)
d_loc_district = {
    'Distrito Salamanca': 0, 
    'Distrito Tetuán': 1, 
    'Distrito Usera': 2, 
    'Distrito San Blas': 3, 
    'Distrito Vicálvaro': 4, 
    'Distrito Villaverde': 5
    # Todos los demás (incluyendo 'loc_district') se mapean a NaN/0
}

# Mapeo 'loc_neigh' (Altamente Simplificado)
d_loc_neigh = {
    'Barrio Lista': 1, 
    'Barrio Recoletos': 2, 
    'Barrio San Andrés': 3, 
    'Barrio Butarque': 4,
    'loc_neigh': 0 # Inválido
    # Todos los demás se mapean a NaN/0
}

# --- 2. Carga de Datos y Preprocesamiento ---
file_name = "Docs/houses_madrid.csv"
try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    print(f"Error: Asegúrate de que el archivo '{file_name}' exista.")
    exit()

# ⚠️ LIMPIEZA DE COLUMNA 'price' (Solución al error anterior)
df['price'] = df['price'].astype(str).str.replace(r'[^\d\.]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.dropna(subset=['price'], inplace=True)
y = df['price'] 

# Definir las columnas características, usando 'room_num'
columnas_caracteristicas = [
    "balcony", "bath_num", "condition", "floor", "garage", "garden", 
    "ground_size", "house_type", "lift", "loc_city", "loc_district", "loc_neigh", 
    "m2_real", "swimming_pool", "terrace", "unfurnished"
]

columnas_existentes = [col for col in columnas_caracteristicas if col in df.columns]
X = df[columnas_existentes].copy()

# Aplicar los mapeos
X['condition'] = X['condition'].map(d_condition).fillna(0)
X['house_type'] = X['house_type'].map(d_house_type).fillna(0)
X['loc_city'] = X['loc_city'].map(d_loc_city).fillna(0)
X['loc_district'] = X['loc_district'].map(d_loc_district).fillna(0)
X['loc_neigh'] = X['loc_neigh'].map(d_loc_neigh).fillna(0)
X['garage'] = X['garage'].apply(map_garage).fillna(0)

# Asegurar que las columnas numéricas son floats y rellenar NaNs con 0
numeric_cols = ["balcony", "bath_num", "floor", "garden", "ground_size", "lift", "m2_real", "swimming_pool", "terrace", "unfurnished"]
for col in numeric_cols:
    if col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

# One-Hot Encoding para cualquier columna categórica restante
columnas_categoricas_restantes = X.select_dtypes(include=['object']).columns
X_procesado = pd.get_dummies(X, columns=columnas_categoricas_restantes, dummy_na=False)
X_final = X_procesado.fillna(0)

# --- 3. Separación de Datos y Entrenamiento del Modelo ---
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42
)
 
print("Entrenando el modelo de Bosque Aleatorio para Madrid...")
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
modelo_rf.fit(X_train, y_train)
print("Entrenamiento completado.")

# --- 4. Evaluación del Modelo ---
predictions = modelo_rf.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

print(f"\n--- Resultado de la Evaluación ---")
print(f"Error Absoluto Medio (MAE): {mae:,.2f} [Moneda]")
print(f"En promedio, la predicción se desvía del precio real por {mae:,.2f} unidades.")

# --- 5. Función de Predicción Interactiva ---
def predecir_precio_casa_interactivo(modelo, caracteristicas_modelo, mapeos, mae_eval):
    """
    Recoge datos de la casa por línea de comandos y predice el precio.
    """
    print("\n" + "="*50)
    print("🏠 INGRESE LOS DETALLES DE LA CASA EN MADRID PARA LA PREDICCIÓN 🏠")
    print("="*50)

    datos_usuario = {}
    
    print("\nPor favor, introduzca los siguientes datos:")
    
    try:
        datos_usuario['m2_real'] = float(input("Superficie útil (m2_real): "))
        #datos_usuario['room_num'] = int(input("Número de habitaciones (room_num): "))
        datos_usuario['bath_num'] = int(input("Número de baños (bath_num): "))
        datos_usuario['floor'] = int(input("Piso (floor, 0 para planta baja): "))
        datos_usuario['ground_size'] = float(input("Tamaño del terreno (ground_size, 0 si no aplica): "))
    except ValueError:
        print("ERROR: Los valores numéricos deben ser números. Terminando...")
        return
    
    # Booleanos/Sí-No
    datos_usuario['balcony'] = 1 if input("¿Tiene balcón? (s/n): ").lower() == 's' else 0
    datos_usuario['garden'] = 1 if input("¿Tiene jardín? (s/n): ").lower() == 's' else 0
    datos_usuario['lift'] = 1 if input("¿Tiene ascensor? (s/n): ").lower() == 's' else 0
    datos_usuario['swimming_pool'] = 1 if input("¿Tiene piscina? (s/n): ").lower() == 's' else 0
    datos_usuario['terrace'] = 1 if input("¿Tiene terraza? (s/n): ").lower() == 's' else 0
    datos_usuario['unfurnished'] = 1 if input("¿Está sin amueblar (unfurnished)? (s/n): ").lower() == 's' else 0

    # Categorías (con opciones simplificadas)
    
    # CONDITION

    print("\n--- Estado (condition) ---")
    for k, v in mapeos['condition'].items():
        # Corregido: Intentar convertir v a int. Si falla, es una cadena irrelevante, la saltamos.
        try:
            v_int = int(v)
            if v_int < 99:
                print(f"[{v}] {k}")
        except ValueError:
            # Si 'v' no es convertible a int (es decir, es una cadena como 'condition'), la omitimos.
            continue
            
    datos_usuario['condition'] = int(input(f"Seleccione el número de estado: "))

    # GARAGE (Simplificado)
    print("\n--- Garaje (garage) ---")
    print("[0] No indicado/Inválido")
    print("[1] Plaza de garaje incluida en el precio")
    print("[2] Plaza de garaje con costo adicional")
    datos_usuario['garage'] = int(input(f"Seleccione el número de garaje: "))
    
    # HOUSE_TYPE
    print("\n--- Tipo de casa (house_type) ---")

    for k, v in mapeos['house_type'].items():
        # Corregido: Intentar convertir v a int. Si falla, es una cadena irrelevante, la saltamos.
        try:
            v_int = int(v)
            if v_int < 99:
                print(f"[{v}] {k}")
        except ValueError:
            # Si 'v' no es convertible a int (es decir, es una cadena como 'condition'), la omitimos.
            continue
        
    datos_usuario['house_type'] = int(input(f"Seleccione el número de tipo de casa: "))

    # LOC_CITY
    print("\n--- Ciudad (loc_city) ---")
    for k, v in mapeos['loc_city'].items():
        if v < 99:
            print(f"[{v}] {k}")
    datos_usuario['loc_city'] = int(input(f"Seleccione el número de ciudad: "))

    # LOC_DISTRICT (Simplificado)
    print("\n--- Distrito (loc_district) ---")
    print("[0] Distrito Salamanca, [1] Distrito Tetuán, [2] Distrito Usera, [3] Distrito San Blas")
    print("[4] Distrito Vicálvaro, [5] Distrito Villaverde, [6] Otro/Inválido")
    datos_usuario['loc_district'] = int(input(f"Seleccione el número de distrito: "))
    
    # LOC_NEIGH (Altamente Simplificado)
    print("\n--- Barrio (loc_neigh) ---")
    print("[0] Otro/No indicado/Inválido")
    print("[1] Barrio Lista, [2] Barrio Recoletos, [3] Barrio San Andrés, [4] Barrio Butarque")
    datos_usuario['loc_neigh'] = int(input(f"Seleccione el número de barrio: "))


    # 3. y 4. Conversión a DataFrame y Alineación de Columnas
    df_usuario = pd.DataFrame([datos_usuario])
    df_prediccion = pd.DataFrame(0, index=[0], columns=caracteristicas_modelo)

    for col in df_usuario.columns:
        if col in df_prediccion.columns:
            df_prediccion[col] = df_usuario[col].iloc[0]

    # Asegurarse de tipos de datos
    for col in df_prediccion.columns:
        df_prediccion[col] = df_prediccion[col].astype(X_final[col].dtype)
        
    # 5. Realizar la predicción
    precio_predicho = modelo.predict(df_prediccion)
    
    print("\n" + "="*50)
    print(f"⭐ PRECIO PREDICHO DEL MODELO ⭐")
    print(f"El precio estimado es: **{precio_predicho[0]:,.2f} [Moneda]**")
    print(f"Basado en un Error Absoluto Medio (MAE) de {mae_eval:,.2f}.")
    print("="*50)


# --- 6. Ejecutar la función interactiva ---
mapeos_disponibles = {
    'condition': {v: k for k, v in d_condition.items()}, 
    'house_type': {v: k for k, v in d_house_type.items()},
    'loc_city': {v: k for k, v in d_loc_city.items()},
}
# La línea para ejecutar la predicción interactiva (necesitas ejecutar este código en tu entorno local)
predecir_precio_casa_interactivo(modelo_rf, X_final.columns, mapeos_disponibles, mae)