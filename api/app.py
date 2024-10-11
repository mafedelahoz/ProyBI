from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from pipeline import create_pipeline
import pandas as pd
from io import StringIO, BytesIO
from DataModel import DataModel
import joblib
from Classes import ToDataFrame, ProcessText, Tokenization, Lemmatization, StopWordDeletion, SpecialCharacterFilter, FinalText, Predictions


# Initialize FastAPI
app = FastAPI()

@app.post("/")
def read_root():
   return {"Hello": "World"}


@app.post("/predict/")
def predict(dataModel: DataModel, file_path: str = Query(...)):
    try:
        # Create pipeline with the provided file path
        pipeline = create_pipeline(file_path)
        print("Pipeline loaded successfully.")
        
        pipeline.named_steps['crear_dataframe'].file_path = file_path

        # Make predictions using the pipeline
        prediction = pipeline.predict([])

        if "csv" in file_path:
            output = StringIO()
            prediction.to_csv(output, index=False)
            output.seek(0)  # Move to the start of the stream
            return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=prediction.csv"})
        
        # Excel (XLSX) Response
        elif "xlsx" in file_path:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                prediction.to_excel(writer, index=False)
            output.seek(0)  # Move to the start of the stream
            return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=prediction.xlsx"})
        
        # JSON Response
        elif "json" in file_path:
            return JSONResponse(content=prediction.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

