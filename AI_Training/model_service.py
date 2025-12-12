import random
import pandas as pd
import numpy as np
import os

MODEL_FEATURES = pd.Index([
    'm2_real', 'room_num', 'bath_num', 'balcony', 'floor', 'garage', 'garden', 
    'ground_size', 'lift', 'swimming_pool', 'terrace', 'unfurnished', 
    'condition', 'house_type', 'loc_city', 'loc_district', 'loc_neigh', 
    'age', 'energy_cert'
])

D_MAPPINGS = {
    'condition': {'new': 1, 'good': 2, 'needs_renovation': 3, 'old': 4},
    'house_type': {'apartment': 1, 'house': 2, 'penthouse': 3},
    'loc_city': {'madrid': 100, 'barcelona': 200, 'valencia': 300},
    'loc_district': {'centro': 10, 'chueca': 20, 'gracia': 30},
    'loc_neigh': {'sol': 1, 'gotic': 2, 'ruzafa': 3},
    'energy_cert': {'a': 1, 'b': 2, 'c': 3, 'g': 7},
}

MAE = 15500.50 

class MockRandomForestModel:
    def predict(self, df):
        """Simula una predicción, devolviendo un precio fijo + un pequeño ruido."""
        base_price = 250000 
        noise = random.uniform(-10000, 10000) 
        return [base_price + noise]

try:
    modelo_rf = MockRandomForestModel()
    print("DEBUG: Modelo de Random Forest simulado cargado correctamente.")
except Exception as e:
    print(f"ERROR al cargar el modelo ML (se usa el mock): {e}")
    modelo_rf = MockRandomForestModel()