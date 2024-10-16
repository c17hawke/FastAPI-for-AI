from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import numpy as np
from .config import Config

router = APIRouter(tags=["Predict Route"])

class PredictionInput(BaseModel):
    data: list[tuple[float, float, float, float]]

@router.post("/predict")
async def predict(data: PredictionInput) -> JSONResponse:
    try:
        model = joblib.load(Config.model_filepath)
        # Make predictions using the loaded model
        input_data = np.array(data.data)

        predictions = model.predict(input_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "predictions": predictions.tolist()
            }
        )
    except Exception as exe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exe)
        )
