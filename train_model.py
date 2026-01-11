import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# 1. Load dataset (IMPORTANT: separator=';')
data = pd.read_csv("data/student-mat.csv", sep=";")

# 2. Feature engineering
data["avg_score"] = (data["G1"] + data["G2"]) / 2

# 3. Pseudo-labeling (AT RISK)
# At risk if failures >= 2 OR avg_score < 10 (out of 20)
data["at_risk"] = ((data["failures"] >= 2) | (data["avg_score"] < 10)).astype(int)

# 4. Select features
X = data[["failures", "absences", "studytime", "avg_score"]]
y = data["at_risk"]

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 7. Evaluate
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# 8. Save model
joblib.dump(model, "risk_model.pkl")

print("✅ Model trained and saved as risk_model.pkl")
