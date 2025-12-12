import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# --- 1. FEATURES QUE SÍ VAS A USAR ---
MODEL_FEATURES = [
    'm2_real', 'room_num', 'bath_num', 'balcony', 'floor', 'garage', 'garden',
    'ground_size', 'lift', 'swimming_pool', 'terrace', 'unfurnished',
    'condition', 'house_type', 'loc_city'
]

# --- 2. MAPEOS DE VARIABLES CATEGÓRICAS ---
D_MAPPINGS = {
    'condition': {
        'new': 1, 'good': 2, 'needs_renovation': 3, 'old': 4,
        'segunda mano/buen estado': 2,
        'segunda mano/a reformar': 3,
        'obra nueva': 1
    },
    'house_type': {
        'piso': 1, 'casa': 2, 'casa o chalet independiente': 2, 'ático': 3,
        'apartment': 1, 'house': 2, 'penthouse': 3
    },
    'loc_city': {
        'vilafranca del penedès': 900,
        'madrid': 100,
        'barcelona': 200,
        'valencia': 300
    }
}

TARGET_COLUMN = 'price'


# --- 3. PREPROCESAMIENTO ---
def preprocess_data(df):
    df_copy = df.copy()

    TARGET_CITY_NAME = 'vilafranca del penedès'
    TARGET_CITY_CODE = 900

    df_copy['loc_city_clean'] = df_copy['loc_city'].astype(str).str.lower().str.strip()

    df_filtered = df_copy[df_copy['loc_city_clean'] == TARGET_CITY_NAME].copy()
    if df_filtered.empty:
        raise ValueError(f"No hay datos para '{TARGET_CITY_NAME}'")

    df_filtered.drop(columns=['loc_city_clean'], errors='ignore', inplace=True)

    for col in ['bath_num', 'room_num']:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

    for col, mapping in D_MAPPINGS.items():
        if col in df_filtered.columns:
            df_filtered[col] = (
                df_filtered[col].astype(str).str.lower().map(mapping).fillna(0)
            )

    df_filtered['loc_city'] = TARGET_CITY_CODE

    X = pd.DataFrame(0, index=df_filtered.index, columns=MODEL_FEATURES)
    for col in MODEL_FEATURES:
        if col in df_filtered.columns:
            X[col] = df_filtered[col].fillna(0)

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    Y = df_filtered[TARGET_COLUMN].copy()

    valid_idx = Y[Y > 1000].index
    X = X.loc[valid_idx]
    Y = Y.loc[valid_idx]

    if X.empty:
        raise ValueError("Tras limpiar, no quedan datos válidos para entrenar.")

    return X, Y


# --- 4. ENTRENAR Y GUARDAR EL MODELO ---
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
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, Y)

    joblib.dump(model, "random_forest_model.pkl")
    print("Modelo guardado como random_forest_model.pkl")


# --- 5. EJECUCIÓN ---
if __name__ == "__main__":
    train_and_save_model("Docs/houses_barcelona.csv")
