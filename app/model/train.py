import json
from datetime import date
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from pathlib import Path
# load data
def train():
    BASE_DIR = Path(__file__).resolve().parents[2]
    data_path = BASE_DIR / "data" / "synthetic_transactions.csv"
    df = pd.read_csv(data_path)
    X = df.drop("fraud_label", axis=1)
    y = df["fraud_label"]
    # stratify=y ensures that the train and test sets have the same proportion of fraud cases as the original dataset, which is important for imbalanced datasets like this one.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        ))
    ])

    pipeline.fit(X_train, y_train)

    print(classification_report(y_test, pipeline.predict(X_test)))

    y_prob = pipeline.predict_proba(X_test)[:, 1]
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    # Lower threshold
    threshold = 0.3
    y_pred_adjusted = (y_prob >= threshold).astype(int)

    print("Threshold:", threshold)
    print(classification_report(y_test, y_pred_adjusted))

    MODEL_DIR = BASE_DIR / "app" / "model"/ "artifacts"

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODEL_DIR / "fraud_detection_model.pkl"

    joblib.dump(pipeline, model_path)

    print("Model saved to:", model_path)

    metadata = {
    "model_type": "RandomForest",
    "version": "1.0",
    "threshold": 0.3,
    "features": list(X.columns),
    "fraud_rate": float(y.mean()),
    "training_date": str(date.today()),
}

    with open(MODEL_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("Model and metadata saved successfully.")

if __name__ == "__main__":
    train()