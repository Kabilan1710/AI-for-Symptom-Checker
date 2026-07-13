# AI Symptom Checker — Demo

## Features (demo)
- Free-text symptom input + quick-pick symptoms
- Differential diagnosis: top-N conditions with confidence bars
- Simple triage: Home / Doctor / ER using keyword rules
- Mock nearby doctor suggestions (JSON) — replace with Google Places for live data
- Attractive Streamlit UI with custom CSS and body diagram placeholder

## How to run (local)
1. Create a virtual env (recommended)
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

markdown
Copy code

2. Install dependencies
pip install -r requirements.txt

markdown
Copy code

3. Train the demo model
cd training
python train_model.py
cd ..

markdown
Copy code

4. Run Streamlit app
streamlit run app.py

pgsql
Copy code

## Files
- `training/train_model.py` — small script to train a MultinomialNB model with `data/symptoms_conditions.csv`.
- `model/symptom_model.pkl` — created after training.
- `backend/` — model loader, predictor, triage, and doctor finder.
- `assets/style.css` — custom styling for a nicer UI.

## To improve / next steps
- Use a larger, medically-vetted dataset (e.g., public symptom-condition datasets).
- Replace static doctor JSON with Google Places API or FHIR-backed directory.
- Add authentication & encrypted storage for personal profiles.
- Add multilingual support and a voice input option.
