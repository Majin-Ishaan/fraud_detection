import numpy as np
from app.model.loadmodel import model, threshold, features

def predict_transaction(data: dict) -> dict:
    row = []
    
    for feature in features:
        if feature not in data:
            raise ValueError(f"Missing feature: {feature}")
        row.append(data[feature])

    input_data = np.array([row])

    prob = model.predict_proba(input_data)[0][1]
    is_fraud = prob >= threshold

    return {
        "fraud_probability": float(prob),
        "is_fraud": bool(is_fraud)
    }