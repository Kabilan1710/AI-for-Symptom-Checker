# backend/doctor_finder.py
import json
from pathlib import Path

_DOCTOR_PATH = Path("data/doctor_list.json")

def get_nearby_doctors(condition: str):
    if not condition:
        return []
    try:
        with open(_DOCTOR_PATH) as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    # basic normalization
    key = condition.lower()
    # direct match or fallback to contains
    if key in data:
        return data[key]
    # fuzzy fallback: check if a key is contained in condition
    for k, v in data.items():
        if k in key or key in k:
            return v
    # else return empty
    return []
