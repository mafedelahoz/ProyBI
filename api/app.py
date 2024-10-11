from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import load_pipeline, predict


# Initialize FastAPI
app = FastAPI()

prediction_model = 
# Load the pipeline (which includes the prediction model)
pipeline = load_pipeline()

# Define the input format
class DataInput(BaseModel):
    features: list[float]  # A list of input features

# Define the prediction endpoint
@app.post("/predict/")
def get_prediction(data: DataInput):
    try:
        # Make prediction using the full pipeline
        prediction = predict(data.features, pipeline)
        return {"prediction": prediction.tolist()}  # Convert numpy array to list
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

