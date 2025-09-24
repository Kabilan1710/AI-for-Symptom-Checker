# backend/triage.py
import json
from pathlib import Path
import re

_RULES_PATH = Path("data/triage_rules.json")

def load_rules():
    if not _RULES_PATH.exists():
        # default simple rules
        return {
            "er_keywords": ["chest pain", "difficulty breathing", "shortness of breath", "unconscious", "severe bleeding"],
            "doctor_keywords": ["fever", "persistent cough", "high fever", "vomiting", "dizziness"],
            "home_keywords": ["mild cough", "runny nose", "sore throat", "mild headache"]
        }
    with open(_RULES_PATH) as f:
        return json.load(f)

def assess_urgency(symptoms_text: str, age: int = 30, medical_history: str = "", body_part: str = "None"):
    """
    Returns one of: "home", "doctor", "er", or "unknown"
    Uses keyword matching and simple age/history heuristics.
    """
    rules = load_rules()
    text = (symptoms_text or "").lower()
    history = (medical_history or "").lower()

    # immediate ER keywords
    for kw in rules.get("er_keywords", []):
        if kw in text:
            return "er"

    # age and history escalation (example)
    if age >= 65 and any(w in text for w in ["fever", "weakness", "confusion"]):
        return "doctor"

    # if history contains serious conditions, escalate
    if any(cond in history for cond in ["heart", "cardiac", "cancer", "transplant"]):
        # if any concerning symptom in text
        if any(w in text for w in ["chest", "shortness", "bleed", "severe"]):
            return "er"
        return "doctor"

    # check doctor keywords
    for kw in rules.get("doctor_keywords", []):
        if kw in text:
            return "doctor"

    # check home keywords
    for kw in rules.get("home_keywords", []):
        if kw in text:
            return "home"

    # body part escalation example
    if body_part.lower() in ["chest", "head"] and any(w in text for w in ["severe", "intense", "sharp"]):
        return "er"

    return "unknown"
