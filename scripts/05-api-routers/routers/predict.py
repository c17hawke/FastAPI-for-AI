from pathlib import Path
from typing import Any
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import numpy as np
from .config import Config

class PredictionInput(BaseModel):
    data: list[tuple[float, float, float, float]]

model = None

def load_model():
    global model
    if model is None:
        model = joblib.load(Config.model_filepath)
        return model
    return model

router = APIRouter(tags=["Predict"])

@router.post("/predict/")
async def predict(data: PredictionInput) -> dict[str, Any]:
    model = load_model()
    if model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Model not loaded")   
    try:
        # Convert input data to NumPy array for prediction
        input_data = np.array(data.data)
        
        # Make predictions
        predictions = model.predict(input_data)
        
        return JSONResponse(content={"predictions": predictions.tolist()})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
