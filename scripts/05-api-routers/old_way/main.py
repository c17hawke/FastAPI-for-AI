from pathlib import Path
from typing import Any
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

app = FastAPI()

# Model storage
model_filepath = Path("model.joblib")
confusion_matrix_path = Path("confusion_matrix.png")

class PredictionInput(BaseModel):
    data: list[tuple[float, float, float, float]]

@app.post("/train/")
async def train_model(file: UploadFile = File(...)) -> dict[str, str]:
    global model
    try:
        # Load CSV file into DataFrame
        df = pd.read_csv(file.file)
        # Assuming the last column is the target variable
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train a Random Forest Classifier
        model = RandomForestClassifier()
        model.fit(X_train.values, y_train.values)
        
        # Make predictions and calculate accuracy
        predictions = model.predict(X_test)

        # Calculate accuracy score
        acc_score = accuracy_score(y_test, predictions)
        
        # Calculate F1 score
        f1 = f1_score(y_test, predictions, average='weighted')
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, predictions)
        
        # Save confusion matrix as an image
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.savefig(confusion_matrix_path)
        plt.close()

        # Save the trained model
        joblib.dump(model, model_filepath)
        
        return JSONResponse(content={"message": f"Model trained successfully with acc_score: {acc_score}! and f1_score: {f1}"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/predict/")
async def predict(data: PredictionInput) -> dict[str, Any]:
    model = joblib.load(model_filepath)    
    try:
        # Convert input data to NumPy array for prediction
        input_data = np.array(data.data)
        
        # Make predictions
        predictions = model.predict(input_data)
        
        return JSONResponse(content={"predictions": predictions.tolist()})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
