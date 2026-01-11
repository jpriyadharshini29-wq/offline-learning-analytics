import joblib
import numpy as np

# Load trained ML model
model = joblib.load("risk_model.pkl")

def predict_risk(failures, absences, studytime, avg_score):
    """
    Returns:
    1 -> At Risk
    0 -> Normal
    """
    features = np.array([[failures, absences, studytime, avg_score]])
    prediction = model.predict(features)[0]
    return int(prediction)
