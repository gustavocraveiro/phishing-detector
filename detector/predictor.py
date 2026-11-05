from pathlib import Path

import joblib
import pandas as pd

from .analyzer import extract_features


# Model path
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "phishing_model.pkl"


# Load trained model and feature columns
model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
MODEL_FEATURE_COLUMNS = model_data["feature_columns"]


def predict_url(url):

    # Extract URL features
    features = extract_features(url)

    data = pd.DataFrame([features], columns=MODEL_FEATURE_COLUMNS)

    # Predict URL classification
    prediction = model.predict(data)[0]

    # Get prediction probabilities
    probabilities = model.predict_proba(data)[0]

    # Map probabilities to their respective classes
    class_probabilities = dict(zip(model.classes_, probabilities))

    confidence = class_probabilities[prediction]

    # Classification result
    result = {
        "url": url,
        "prediction": "Phishing" if prediction == 1 else "Legitimate",
        "confidence": round(float(confidence) * 100, 2)
    }

    return result
