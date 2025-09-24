# backend/predictor.py
from .model_loader import load_model
import numpy as np
import re

_model, _vectorizer = load_model()

def clean_input(text: str) -> str:
    text = text or ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s,]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_top_conditions(symptom_text: str, top_n: int = 3):
    """
    Returns a list of tuples (condition, probability) sorted by probability desc.
    """
    text = clean_input(symptom_text)
    if not text:
        return []
    X = _vectorizer.transform([text])
    # Check if model has predict_proba
    try:
        probs = _model.predict_proba(X)[0]
        classes = _model.classes_
        # pair & sort
        paired = list(zip(classes, probs))
        paired.sort(key=lambda x: x[1], reverse=True)
        top = paired[:top_n]
        # ensure probabilities are floats
        return [(str(c), float(p)) for c, p in top]
    except Exception:
        # fallback to predict only (no probabilities)
        pred = _model.predict(X)[0]
        return [(str(pred), 0.6)]
