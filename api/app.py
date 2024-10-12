from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from pipeline import create_pipeline
import pandas as pd
from io import StringIO, BytesIO
from DataModel import DataModel
import os
import json
# from backend.model import ToDataFrame
import joblib

# Initialize FastAPI
app = FastAPI()

@app.post("/")
def read_root():
   return {"Hello": "World"}

UPLOAD_DIR = "./uploads"

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Create pipeline with the provided file path
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        
        # Guardar el archivo subido
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # Crear el pipeline con la ruta del archivo
        pipeline = create_pipeline(file_location)
        print("Pipeline loaded successfully.")
        
        # Make predictions using the pipeline
        prediction = pipeline.predict([])

        if "csv" in file.filename:
            output = StringIO()
            prediction.to_csv(output, index=False)
            output.seek(0)
            return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=prediction.csv"})
        
        elif "xlsx" in file.filename:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                prediction.to_excel(writer, index=False)
            output.seek(0)
            return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=prediction.xlsx"})
        
        elif "json" in file.filename:
            return JSONResponse(content=prediction.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Reentranamiento del modelo
# @app.post("/reentrenar-con-archivo/")
# async def reentrenar_modelo_con_archivo(file: UploadFile = File(...)):
#     try:
#         # Obtener la extensión del archivo para determinar su tipo
#         filename = file.filename
#         if filename.endswith('.csv'):
#             print("Cargando datos desde archivo CSV...")
#             contenido = await file.read()
#             nuevos_datos_df = pd.read_csv(pd.compat.StringIO(contenido.decode('utf-8')))
#         elif filename.endswith('.xlsx'):
#             print("Cargando datos desde archivo Excel...")
#             contenido = await file.read()
#             nuevos_datos_df = pd.read_excel(contenido)
#         elif filename.endswith('.json'):
#             print("Cargando datos desde archivo JSON...")
#             contenido = await file.read()
#             json_data = json.loads(contenido.decode('utf-8'))
#             nuevos_datos_df = pd.DataFrame(json_data)
#         else:
#             raise HTTPException(status_code=400, detail="Formato de archivo no soportado. Por favor, usa CSV, XLSX o JSON.")

#         datos_existentes_path = "ODScat_345.xlsx"
#         if os.path.exists(datos_existentes_path):
#             datos_existentes = pd.read_excel(datos_existentes_path)
#         else:
#             raise HTTPException(status_code=404, detail="Archivo de datos existentes no encontrado")

#         # Verificar que las columnas coincidan entre los nuevos y los existentes
#         if set(datos_existentes.columns) != set(nuevos_datos_df.columns):
#             raise HTTPException(status_code=400, detail="Las columnas de los nuevos datos no coinciden con los datos existentes")

#         datos_combinados = pd.concat([datos_existentes, nuevos_datos_df], ignore_index=True)

#         preprocesador = ToDataFrame()
#         datos_procesados = preprocesador.fit_transform(datos_combinados)

#         X = datos_procesados.drop('sdg', axis=1)  
#         y = datos_procesados['sdg']

#         # Dividir en conjuntos de entrenamiento y prueba
#         from sklearn.model_selection import train_test_split
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#         # Reentrenar el modelo con los datos combinados
#         from sklearn.pipeline import Pipeline
#         from sklearn.preprocessing import StandardScaler
#         from sklearn.naive_bayes import MultinomialNB

#         pipeline = Pipeline([
#             ('scaler', StandardScaler()),
#             ('model', MultinomialNB())
#         ])

#         pipeline.fit(X_train, y_train)

#         # Evaluar el modelo
#         from sklearn.metrics import accuracy_score
#         y_pred = pipeline.predict(X_test)
#         precision = accuracy_score(y_test, y_pred)
#         print(f'Precisión del modelo actualizado: {precision}')

#         # Guardar el modelo actualizado
#         joblib.dump(pipeline, '../pipeline_model.pkl')

#         return {"message": "Modelo reentrenado con éxito", "precision": precision}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

