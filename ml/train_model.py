import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
DATA_PATH = os.path.join(BASE_DIR, "data", "churn_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "churn_model.pkl")

# Load data
df = pd.read_csv(DATA_PATH)

X = df.drop("churn", axis=1)
y = df["churn"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, MODEL_PATH)

print("✅ churn_model.pkl CREATED SUCCESSFULLY")
print("📍 Saved at:", MODEL_PATH)
