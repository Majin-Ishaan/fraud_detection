import joblib
import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
MODEL_DIR = _HERE / "artifacts"

model = joblib.load(MODEL_DIR / "fraud_detection_model.pkl")

with open(MODEL_DIR / "metadata.json") as f:
    metadata = json.load(f)

threshold : float = metadata["threshold"]
features : list[str] = metadata["features"]