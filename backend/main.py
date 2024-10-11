from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import pickle
import os

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

import joblib

# Cargar el modelo con joblib
model = joblib.load("model.pkl")

# Endpoint para subir archivos CSV/Excel y hacer predicciones
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    if file.filename.endswith(".csv"):
        df = pd.read_csv(file_location)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file_location)
    else:
        return JSONResponse(content={"error": "File type not supported"}, status_code=400)

    # Usar el modelo cargado desde el archivo .pkl para hacer predicciones
    predictions = model.predict(df)  # Asumiendo que `df` tiene el formato correcto para el modelo

    return JSONResponse(content={"predictions": predictions.tolist()})

# Endpoint para clasificar un texto
class TextInput(BaseModel):
    text: str

@app.post("/classify-text/")
async def classify_text(input: TextInput):
    # Preprocesar el texto si es necesario (según el modelo)
    # Convertir el texto a un formato que el modelo pueda usar (esto depende de tu pipeline)

    # Aquí debes convertir el texto a las características que usa tu modelo
    # Esto podría ser un `vectorizer.transform` si estás usando un modelo de NLP
    # Por ejemplo, si usas un TfidfVectorizer:
    # features = vectorizer.transform([input.text])
    # prediction = model.predict(features)

    prediction = model.predict([input.text])  # Asumiendo que el modelo puede procesar directamente el texto
    return JSONResponse(content={"prediction": prediction[0]})

# Endpoint para reentrenar el modelo
@app.post("/retrain-model/")
async def retrain_model():
    # Simular reentrenamiento del modelo con datos (aquí pondrías la lógica real)
    # Por ejemplo, podrías cargar nuevos datos de entrenamiento y entrenar el modelo nuevamente

    # df_train = pd.read_csv("nuevos_datos.csv")  # Cargar nuevos datos para el entrenamiento
    # X_train, y_train = ...  # Separar características y etiquetas
    # model.fit(X_train, y_train)  # Reentrenar el modelo

    # Guardar el modelo nuevamente
    # with open("model.pkl", "wb") as file:
    #     pickle.dump(model, file)

    return JSONResponse(content={"message": "Modelo reentrenado exitosamente"})

