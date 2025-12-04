import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

try:
    df = pd.read_csv("/Docs/houses_barcelona.csv")
except FileNotFoundError:
    print("Error: Asegúrate de que el archivo 'houses_barcelona.xlsx' exista.")


y = df['price'] 

columnas_caracteristicas = [
    "balcony", "bath_num", "condition", "floor", "garage", "garden", 
    "ground_size", "house_type", "lift", "loc_city", "loc_district", "loc_neigh", 
    "m2_real", "room_numbers", "swimming_pool", "terrace", "unfurnished"
]

X = df[columnas_caracteristicas]

d = {'promoción de obra nueva': 0, 'segunda mano/a reformar': 1, 'segunda mano/buen estado': 2, 'segunda mano/reformado': 3}
df['condition'] = df['condition'].map(d)
d = {'no indicado': 0, 'plaza de garaje incluida en el precio': 1, 'plaza de garaje por 10.000 eur adicionales': 2, 'plaza de garaje por 12.000 eur adicionales': 3, 'plaza de garaje por 5.000 eur adicionales': 4, 'plaza de garaje por 6.000 eur adicionales': 5, 'plaza de garaje por 8.000 eur adicionales': 6}
df['garage'] = df['garage'].map(d)
d = {'Apartamento': 0, 'Casa o chalet independiente': 1, 'Casa o chalet adosado': 2, 'Estudio': 3, 'Finca rústica': 4, 'Piso': 5}
df['house_type'] = df['house_type'].map(d)
d = {'Barcelona': 0, 'Hospitalet de Llobregat': 1, 'Vilafranca del Penedès': 2}
df['loc_city'] = df['loc_city'].map(d)
d = {'Distrito Centre Vila': 0, 'Distrito Eixample': 1, 'Distrito La Escorxador': 2, 'Distrito Sant Julià': 3, 'Distrito Sant Pere': 4, 'Distrito Sants-Badal': 5}
df['loc_district'] = df['loc_district'].map(d)
d = {'La Barceloneta': 0, 'La Florida': 1, 'Les Corts': 2, 'Llefia': 3, 'Navas': 4, 'Sant Marti': 5, 'Sant Pere': 6, 'Sant Julià': 7, 'Sants-Badal': 8, 'Vilafranca del Penedès': 9}
df['loc_neigh'] = df['loc_neigh'].map(d)


columnas_categoricas = X.select_dtypes(include=['object']).columns

X_procesado = pd.get_dummies(X, columns=columnas_categoricas, dummy_na=False)


X_final = X_procesado.fillna(0)

df.dropna(subset=['price'], inplace=True)
y = df['price']


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