# backend/model_loader.py
import pickle
from pathlib import Path

_MODEL_PATH = Path("model/symptom_model.pkl")

def load_model(path: str = None):
    p = Path(path) if path else _MODEL_PATH
    if not p.exists():
        raise FileNotFoundError(f"Model file not found: {p.resolve()}. Run training/train_model.py first.")
    with p.open("rb") as f:
        obj = pickle.load(f)
    # Expect {"model": model, "vectorizer": vectorizer}
    return obj["model"], obj["vectorizer"]
