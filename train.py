from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from detector.analyzer import extract_features, FEATURE_COLUMNS


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "urls.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "phishing_model.pkl"


def load_dataset():

    df = pd.read_csv(DATASET_PATH)

    required_columns = {"url", "label"}

    if not required_columns.issubset(df.columns):
        raise ValueError("Dataset must contain 'url' and 'label' columns.")

    df = df.dropna(subset=["url", "label"])
    df["url"] = df["url"].astype(str).str.strip()
    df = df[df["url"] != ""]

    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])

    df = df[df["label"].isin([0, 1])]
    df = df.drop_duplicates(subset=["url"])

    if df["label"].nunique() != 2:
        raise ValueError("Dataset must contain both classes: 0 and 1.")

    if df["label"].value_counts().min() < 2:
        raise ValueError("Each class needs at least two samples.")

    return df


def prepare_data(df):

    X = pd.DataFrame(
        [extract_features(url) for url in df["url"]],
        columns=FEATURE_COLUMNS
    )

    y = df["label"].astype(int)

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


def train_model(X_train, y_train):

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    print("\n===== MODEL EVALUATION =====")

    print(f"Accuracy:  {accuracy_score(y_test, predictions):.4f}")
    print(f"Precision: {precision_score(y_test, predictions, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_test, predictions, zero_division=0):.4f}")
    print(f"F1-score:  {f1_score(y_test, predictions, zero_division=0):.4f}")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=["Legitimate", "Phishing"],
        zero_division=0
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))


def save_model(model):

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS
        },
        MODEL_PATH
    )

    print(f"\nModel saved successfully: {MODEL_PATH}")


def main():

    print("===== PHISHING DETECTOR - MODEL TRAINING =====")

    print("\n[1] Loading dataset...")
    df = load_dataset()

    print(f"Dataset samples: {len(df)}")

    print("\n[2] Preparing features...")
    X_train, X_test, y_train, y_test = prepare_data(df)

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    print("\n[3] Training Random Forest model...")
    model = train_model(X_train, y_train)

    print("\n[4] Evaluating model...")
    evaluate_model(model, X_test, y_test)

    print("\n[5] Saving model...")
    save_model(model)

    print("\nTraining completed successfully!")


if __name__ == "__main__":
    main()
