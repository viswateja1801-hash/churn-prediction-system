import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "churn_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "churn_data.csv")

def train_and_save_model():
    df = pd.read_csv(DATA_PATH)

    X = df.drop("churn", axis=1)
    y = df["churn"]

    model = LogisticRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return model

# 🔥 AUTO-FIX: train model if missing
if not os.path.exists(MODEL_PATH):
    model = train_and_save_model()
else:
    model = joblib.load(MODEL_PATH)

def predict_churn(tenure, monthly, total, calls):
    prob = model.predict_proba([[tenure, monthly, total, calls]])[0][1]

    if prob >= 0.7:
        risk = "HIGH"
    elif prob >= 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return round(prob * 100, 2), risk
