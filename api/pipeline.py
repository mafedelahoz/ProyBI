import pickle
import numpy as np

# Load the pipeline that includes preprocessing and prediction model
def load_pipeline(pipeline_path="pipeline_model.pkl"):
    with open(pipeline_path, 'rb') as f:
        pipeline = pickle.load(f)
    return pipeline

# Use the pipeline to make predictions
def predict(data, pipeline):
    # Assuming data is a list of input features
    data = np.array(data).reshape(1, -1)
    prediction = pipeline.predict(data)  # Use the entire pipeline to predict
    return prediction
