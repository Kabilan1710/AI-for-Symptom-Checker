# training/train_model.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
from pathlib import Path
from utils import clean_text

DATA_PATH = Path("../data/symptoms_conditions.csv")
MODEL_OUT = Path("../model/symptom_model.pkl")

def main():
    df = pd.read_csv(DATA_PATH)
    # Ensure columns exist
    df = df.rename(columns={df.columns[0]: "symptoms", df.columns[1]: "condition"})
    df["symptoms"] = df["symptoms"].astype(str).apply(clean_text)
    X = df["symptoms"]
    y = df["condition"].astype(str)

    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)

    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_OUT, "wb") as f:
        pickle.dump({"model": model, "vectorizer": vectorizer}, f)

    print(f"Model saved to {MODEL_OUT.resolve()}")

if __name__ == "__main__":
    main()
