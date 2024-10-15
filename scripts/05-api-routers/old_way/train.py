import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load the iris dataset
df = pd.read_csv('iris.csv')
print(df.head())

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
plt.savefig("./confusion_matrix.png")
plt.close()

# Save the trained model
joblib.dump(model, "./iris_model.joblib")

print(f"Model trained successfully with acc_score: {acc_score}! and f1_score: {f1}")
