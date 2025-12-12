import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# --------------------------------------------------------------------
# FEATURES usados en el modelo (IGUALES que model_service)
# --------------------------------------------------------------------
MODEL_FEATURES = [
    'm2_real', 'room_num', 'bath_num', 'balcony', 'floor', 'garage', 'garden',
    'ground_size', 'lift', 'swimming_pool', 'terrace', 'unfurnished',
    'condition', 'house_type', 'loc_city'
]

# --------------------------------------------------------------------
# MAPEOS (IGUALES que model_service.py)
# --------------------------------------------------------------------
D_MAPPINGS = {
    'condition': {
        'new': 0,
        'segunda mano/buen estado': 2,
        'segunda mano/a reformar': 1,
        'reformar': 3
    },

    'house_type': {
        'apartamento': 0,
        'finca rústica': 4,
        'chalet adosado': 2,
        'estudio': 3,
        'chalet independiente': 1,
        'piso': 5,
    },

    'loc_city': {
        'avinyonet del penedès': 0,
        'castellví de la marca': 1,
        'el pla del penedès': 2,
        'font-rubí': 3,
        'gelida': 4,
        'la granada': 5,
        'les cabanyes': 6,
        'mediona': 7,
        'olèrdola': 8,
        'pacs del penedès': 9,
        'pontons': 10,
        'puigdàlber': 11,
        'sant cugat sesgarrigues': 12,
        "sant llorenç d'hortons": 13,
        'sant martí sarroca': 14,
        'sant pere de riudebitlles': 15,
        'sant quintí de mediona': 16,
        "sant sadurní d'anoia": 17,
        'santa margarida i els monjos': 18,
        'subirats': 19,
        'torrelavit': 20,
        'torrelles de foix': 21,
        'vilafranca del penedès': 22,
        'vilobí del penedès': 23
    }
}

TARGET_COLUMN = 'price'


# --------------------------------------------------------------------
# PREPROCESAMIENTO (ADAPTADO para usar TODAS las ciudades)
# --------------------------------------------------------------------
def preprocess_data(df):

    df_copy = df.copy()

    # Normalizar ciudad
    df_copy['loc_city_clean'] = df_copy['loc_city'].astype(str).str.lower().str.strip()

    # Mapear TODAS las ciudades disponibles
    df_copy['loc_city'] = df_copy['loc_city_clean'].map(D_MAPPINGS['loc_city']).fillna(-1)

    # Filtrar solo entradas válidas
    df_copy = df_copy[df_copy['loc_city'] >= 0]

    df_copy.drop(columns=['loc_city_clean'], inplace=True)

    # Convertir numéricos
    for col in ['bath_num', 'room_num']:
        if col in df_copy.columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')

    # Aplicar mappings categóricos restantes
    for col, mapping in D_MAPPINGS.items():
        if col in df_copy.columns and col != 'loc_city':
            df_copy[col] = df_copy[col].astype(str).str.lower().map(mapping).fillna(0)

    # Construcción de matriz X
    X = pd.DataFrame(0, index=df_copy.index, columns=MODEL_FEATURES)
    for col in MODEL_FEATURES:
        if col in df_copy.columns:
            X[col] = df_copy[col].fillna(0)

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    Y = df_copy[TARGET_COLUMN].copy()

    # Filtrar precios razonables > 1000 €
    valid_idx = Y[Y > 1000].index
    X = X.loc[valid_idx]
    Y = Y.loc[valid_idx]

    if X.empty:
        raise ValueError("Tras limpiar, no quedan datos válidos para entrenar.")

    return X, Y


# --------------------------------------------------------------------
# ENTRENAR Y GUARDAR EL MODELO (COMPATIBLE con model_service)
# --------------------------------------------------------------------
def train_and_save_model(data_path):
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo en {data_path}")
        return

    if TARGET_COLUMN not in df.columns:
        print(f"ERROR: No existe la columna '{TARGET_COLUMN}' en el CSV.")
        return

    try:
        X, Y = preprocess_data(df)
    except ValueError as e:
        print(f"ERROR en preprocesamiento: {e}")
        return

    print(f"Entrenando modelo con {len(X)} filas...")

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, Y)

    joblib.dump(model, "random_forest_model.pkl")
    print("Modelo guardado como random_forest_model.pkl")


# --------------------------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------------------------
if __name__ == "__main__":
    train_and_save_model("Docs/houses_barcelona.csv")
