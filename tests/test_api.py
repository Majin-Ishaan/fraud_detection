from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "transaction_amount": 75000.0,
    "transaction_hour": 2,
    "customer_age": 22.0,
    "is_international": 1,
    "past_failed_transactions": 4
}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data
    assert "model_type" in data


def test_predict_returns_fraud_score():
    response = client.post("/predict",json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_probability" in data
    assert "is_fraud" in data
    assert "threshold" in data
    assert 0.0 <= data["fraud_probability"] <= 1.0
    assert isinstance(data["is_fraud"], bool)

def test_rejects_negative_data():
    invalid_payload = VALID_PAYLOAD.copy()
    invalid_payload["transaction_amount"] = -100.0
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422



def test_rejects_negative_hour():
    payload = {**VALID_PAYLOAD, "transaction_hour": 25}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_rejects_invalid_is_international():
    payload = {**VALID_PAYLOAD, "is_international": 5}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_rejects_missing_field():
    payload = {**VALID_PAYLOAD}
    del payload["transaction_amount"]
    response = client.post("/predict", json=payload)
    assert response.status_code == 422