# HOMIE

## 🏠 Descripción del Proyecto

Este proyecto consiste en una API REST desarrollada con **Flask** que permite a los usuarios registrarse, iniciar sesión, obtener predicciones de precios para nuevas propiedades y poder guardarlas para futuros usos. La persistencia de los datos de usuarios y viviendas se maneja a través de una base de datos **MySQL**.

## 🛠️ Archivos del Proyecto

A continuación, una breve explicación de la función de cada archivo en el proyecto:

| Archivo | Descripción |
| :--- | :--- |
| `API.py` | **Punto de entrada de la aplicación.** Define y expone todos los *endpoints* de la API REST (login, registro, CRUD de viviendas, predicción de precio) utilizando Flask, JWT para autenticación y CORS para permitir el acceso desde el frontend. |
| `db_conexion.py` | Módulo central para la gestión de la conexión con la base de datos MySQL. Contiene la función `coneccion_bd()` que establece la conexión. |
| `model_service.py` | Contiene la lógica del modelo de Machine Learning para la predicción de precios. Define las características de entrada (`MODEL_FEATURES`) y los mapeos de categorías (`D_MAPPINGS`). |
| `train_model.py` | Este archivo es el módulo de entrenamiento del modelo de Machine Learning. Su única función es preparar los datos del archivo houses_barcelona.csv, entrenar un modelo de Random Forest para predecir precios de viviendas, y guardar ese modelo en disco (random_forest_model.pkl) para que pueda ser cargado y utilizado por model_service.py en la API.|
| `usuario.py` | **Entidad/Modelo** que representa la estructura de un Usuario, con sus atributos (`id`, `nombre`, `contraseña`, `email`) y métodos *getter*/*setter*. |
| `vivienda.py` | **Entidad/Modelo** que representa la estructura de una Vivienda, con todos sus atributos y métodos *getter*/*setter*. |
| `usuarioDAO.py` | **Data Access Object (DAO)** para la entidad `Usuario`. Contiene la lógica para interactuar directamente con la tabla `usuario` en la base de datos (e.g., `login`, `register`). |
| `viviendaDAO.py` | **Data Access Object (DAO)** para la entidad `Vivienda`. Contiene la lógica para interactuar directamente con la tabla `vivienda` en la base de datos (e.g., `insertVivienda`, `deleteVivienda`, `selectViviendasByUser`). |
| `db_homie.sql` | **Script SQL** con el esquema de la base de datos. Contiene las sentencias `CREATE SCHEMA` y `CREATE TABLE` para las tablas `usuario` y `vivienda`. |
| `houses_barcelona.csv` | Archivo CSV con un dataset de viviendas, probablemente utilizado para entrenar o simular el modelo de predicción de precios. |

## 🚀 Pasos para la Configuración y Uso

Sigue estos pasos para poner en marcha la aplicación:

### 1. Configuración de la Base de Datos

1.  **Ejecutar el Script SQL:** Asegúrate de tener un servidor MySQL instalado y funcionando. Luego, ejecuta el archivo **`db_homie.sql`** en tu cliente MySQL (Workbench, DBeaver, línea de comandos, etc.). Esto creará la base de datos con el esquema necesario.

2.  **Cambiar Credenciales de Conexión:** Edita el archivo **`db_conexion.py`** y actualiza el `user` y `password` con las credenciales de tu servidor MySQL.

    ```python
    import mysql.connector

    def coneccion_bd():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="TU_USUARIO_MYSQL",  # <-- ¡CAMBIAR AQUÍ!
                password="TU_CONTRASEÑA_MYSQL",  # <-- ¡CAMBIAR AQUÍ!
                database="homie"
            )
            # ...
    ```

### 2. Instalación de Dependencias (pip)

Es altamente recomendado utilizar un entorno virtual para aislar las dependencias del proyecto.

1.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    # En Linux/macOS:
    source venv/bin/activate
    # En Windows:
    .\venv\Scripts\activate
    ```

2.  **Instalar las librerías necesarias:**
    Ejecuta el siguiente comando para instalar todas las dependencias de Python requeridas:
    ```bash
    pip install Flask pandas numpy mysql-connector-python flask-cors flask-jwt-extended scikit-learn joblib

### 3. Ejecución de la Aplicación

1.  **Iniciar la API:** Ejecuta el archivo principal de la API desde la terminal:
    ```bash
    python API.py
    ```

2.  **Acceso:** La API se iniciará por defecto en `http://127.0.0.1:5000/`. Puedes interactuar con los *endpoints* definidos (`/api/login`, `/api/register`, `/api/vivienda`, `/api/predictPrice`, etc.) utilizando un cliente como Postman.