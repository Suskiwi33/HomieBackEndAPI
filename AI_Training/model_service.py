import random
import pandas as pd
import numpy as np
import os
import joblib

# --------------------------------------------------------------------
# FEATURES utilizados por el modelo entrenado
# --------------------------------------------------------------------
MODEL_FEATURES = pd.Index([
    'm2_real', 'room_num', 'bath_num', 'balcony', 'floor', 'garage', 'garden',
    'ground_size', 'lift', 'swimming_pool', 'terrace', 'unfurnished',
    'condition', 'house_type', 'loc_city'
])

# --------------------------------------------------------------------
# Mapeo de categorías → valores numéricos
# --------------------------------------------------------------------
D_MAPPINGS = {
    'condition': {
        'new': 1, 'good': 2, 'needs_renovation': 3, 'old': 4,
        'segunda mano/buen estado': 2,
        'segunda mano/a reformar': 3,
        'obra nueva': 1
    },
    'house_type': {
        'piso': 1, 'casa': 2, 'ático': 3,
        'apartment': 1, 'house': 2, 'penthouse': 3
    },
    'loc_city': {
        'madrid': 100,
        'barcelona': 200,
        'valencia': 300,
        'vilafranca del penedès': 900
    }
}

MAE = 15500.50

# --------------------------------------------------------------------
# Modelo Mock (solo si falla el modelo real)
# --------------------------------------------------------------------
class MockRandomForestModel:
    def predict(self, df):
        base_price = 250000
        noise = random.uniform(-10000, 10000)
        return [base_price + noise]


# --------------------------------------------------------------------
# Cargar modelo real entrenado
# --------------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "random_forest_model.pkl")

try:
    if os.path.exists(MODEL_PATH):
        modelo_rf = joblib.load(MODEL_PATH)
        print("DEBUG: Modelo REAL RandomForest cargado correctamente.")
    else:
        print("⚠ WARNING: Modelo real no encontrado en:", MODEL_PATH)
        modelo_rf = MockRandomForestModel()
except Exception as e:
    print(f"⚠ ERROR cargando modelo real (usando Mock): {e}")
    modelo_rf = MockRandomForestModel()


# --------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE PREDICCIÓN
# --------------------------------------------------------------------
def predict_price(input_data: dict):

    df = pd.DataFrame([input_data])

    for col in D_MAPPINGS.keys():
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    for col, mapping in D_MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(0)

    X = pd.DataFrame(columns=MODEL_FEATURES)
    for col in MODEL_FEATURES:
        X[col] = [df[col].iloc[0] if col in df.columns else 0]

    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    prediction = modelo_rf.predict(X)[0]

    return {
        "predicted_price": float(prediction),
        "model_mae": MAE
    }
