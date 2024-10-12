from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from pipeline import create_pipeline, retrain
import pandas as pd
from io import StringIO, BytesIO
from DataModel import DataModel
import os
import json
# from backend.model import ToDataFrame
import joblib
from Classes import ToDataFrame, ProcessText, Tokenization, Lemmatization, StopWordDeletion, SpecialCharacterFilter, FinalText, Predictions


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
@app.post("/reentrenar-con-archivo/")
async def reentrenar_modelo_con_archivo(file: UploadFile = File(...)):
    try:
         # Create pipeline with the provided file path
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        
        # Guardar el archivo subido
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # Crear el pipeline con la ruta del archivo
        pipeline = retrain(file_location)
        print("Pipeline loaded successfully.")
        
        # Make predictions using the pipeline
        accuracy = pipeline.fit([])
        return JSONResponse(content=accuracy.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

