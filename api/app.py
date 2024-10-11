from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pipeline import create_pipeline
import pandas as pd


# Initialize FastAPI
app = FastAPI()


# Define the input format
class DataInput(BaseModel):
    features: list[float]  # A list of input features

# Define the prediction endpoint
@app.post("/predict/")
def predict(data: DataInput, file_path: str = Query(...)):
    try:
        # Create pipeline with the provided file path
        pipeline = create_pipeline(file_path)
        
        # Prepare input data as a DataFrame

        # Make predictions using the pipeline
        prediction, probability = pipeline.predict([])

        return {
            "prediction": prediction.tolist(),
            "probability": probability.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

