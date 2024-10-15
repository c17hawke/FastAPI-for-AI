from pathlib import Path

class Config:
    model_filepath = Path("./artifacts/model.joblib")
    confusion_matrix_path = Path("./artifacts/confusion_matrix.png")