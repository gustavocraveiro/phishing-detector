from pathlib import Path
from urllib.parse import urlsplit

import joblib
import pandas as pd
import tldextract

from .analyzer import extract_features, validate_url


# Model path
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "phishing_model.pkl"


# Load trained model and feature columns
model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
MODEL_FEATURE_COLUMNS = model_data["feature_columns"]


def predict_url(url):

# Validate first so invalid URLs still raise ValueError
    if not validate_url(url):
        raise ValueError("Invalid URL provided.")

    # Trusted domains skip the model
    if is_trusted(url):
        return {
            "url": url,
            "prediction": "Legitimate",
            "confidence": None,
            "reason": "Trusted domain"
        }

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


# Institutional suffixes treated as trusted (still not a guarantee of safety)
TRUSTED_SUFFIXES = {"edu.br", "gov.br", "edu", "gov"}

# Well-known domains (extend this list as needed)
TRUSTED_DOMAINS = {
    "google.com",
    "youtube.com",
    "github.com",
    "microsoft.com",
    "wikipedia.org",
}

extractor = tldextract.TLDExtract(suffix_list_urls=())


def is_trusted(url):
    """Return True if the URL belongs to a trusted domain or suffix."""
    parsed = urlsplit(url if "://" in url else f"//{url}")
    extracted = extractor(parsed.hostname or "")

    registered_domain = extracted.registered_domain.lower()
    suffix = extracted.suffix.lower()

    return registered_domain in TRUSTED_DOMAINS or suffix in TRUSTED_SUFFIXES
