# Fraud Detection System

A real-time payment fraud detection API built with FastAPI and a RandomForest classifier.

## Project Structure
fraud_detection/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── model/
│   │   ├── train.py            # Model training script
│   │   ├── loadmodel.py        # Loads model at startup
│   │   └── artifacts/          # Saved model + metadata
│   ├── schemas/
│   │   └── predict.py          # Request validation
│   └── services/
│       └── predict.py          # Prediction logic
├── data/
│   └── synthetic_transactions.csv
├── training/
│   └── generate_synthetic_data.py
├── requirements.txt
└── README.md

## Setup
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Regenerate training data
python training/generate_synthetic_data.py

# Train the model
python app/model/train.py

# Run the API
uvicorn app.main:app --reload

## API Reference

### GET /health
Returns API and model status.

### POST /predict
Request body:
{
  "transaction_amount": 75000.0,
  "transaction_hour": 2,
  "customer_age": 22.0,
  "is_international": 1,
  "past_failed_transactions": 4
}

Response:
{
  "fraud_probability": 0.84,
  "is_fraud": true,
  "threshold": 0.3,
  "model_version": "1.0"
}

## Model Details
- Algorithm: RandomForest (200 estimators, class_weight=balanced)
- Preprocessing: StandardScaler
- Decision threshold: 0.3
- Training data: 10,000 synthetic transactions

## Interactive Docs
Swagger UI: http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc