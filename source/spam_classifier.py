"""
Spam/Ham classifier using Logistic Regression.
Downloads the SMS Spam Collection dataset (UCI ML Repository),
trains a small logistic regression model, and saves it locally.
"""

import urllib.request
import zipfile
import os
import pickle
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))

def download_dataset(dest_dir=HERE):
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
    zip_path = os.path.join(dest_dir, "smsspamcollection.zip")
    print("Downloading SMS Spam Collection dataset...")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(dest_dir)
    os.remove(zip_path)
    print("Dataset ready.")
    return os.path.join(dest_dir, "SMSSpamCollection")


def load_data(filepath):
    texts, labels = [], []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            label, text = line.strip().split("\t", 1)
            labels.append(1 if label == "spam" else 0)
            texts.append(text)
    return texts, labels


def train(texts, labels):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    print("Training logistic regression model...")
    model = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=3000)),
        ("clf",   LogisticRegression(max_iter=1000)),
    ])
    model.fit(texts, labels)
    print("Training complete.")
    return model


def save_model(model, path="spam_model.pkl"):
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {path}")


def load_model(path="spam_model.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)


def predict(model, messages):
    preds = model.predict(messages)
    for pred in preds:
        label = "SPAM" if pred == 1 else "HAM"
        print(label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify a message as SPAM or HAM.")
    parser.add_argument("text", nargs="?", help="Message to classify")
    args = parser.parse_args()

    model_path = os.path.join(HERE, "spam_model.pkl")

    if not os.path.exists(model_path):
        data_file = download_dataset()
        texts, labels = load_data(data_file)
        model = train(texts, labels)
        save_model(model, model_path)
    else:
        model = load_model(model_path)

    if args.text:
        predict(model, [args.text])
    else:
        samples = [
            "Congratulations! You've won a FREE iPhone. Click here to claim now!!!",
            "Hey, are we still meeting for lunch tomorrow?",
            "URGENT: Your bank account has been compromised. Call us immediately.",
            "Can you pick up some milk on your way home?",
        ]
        print("\n--- Predictions ---")
        predict(model, samples)
