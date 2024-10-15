# predict the species of iris flowers using the model trained in train.py
import joblib

# Load the model
model = joblib.load('iris_model.joblib')
print('Model loaded from iris_model.joblib')

# Make predictions using the loaded model
X_test = [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]

predictions = model.predict(X_test)
print('Predictions:', predictions)

