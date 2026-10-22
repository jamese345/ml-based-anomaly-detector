import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib


DATA_PATH = "data/security_events.csv"
MODEL_PATH = "models/isolation_forest.joblib"


FEATURE_COLUMNS = [
    "failed_attempts",
    "successful_logins",
    "login_frequency",
    "unique_source_ips",
    "login_hour",
    "session_duration",
    "request_count"
]


def load_data():
    return pd.read_csv(DATA_PATH)


def prepare_features(df):
    return df[FEATURE_COLUMNS]


def train_model(X):
    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    return model


def save_model(model):
    joblib.dump(model, MODEL_PATH)


def main():
    df = load_data()

    X = prepare_features(df)

    print("=== TRAINING ISOLATION FOREST ===")
    print(f"Training samples: {len(X)}")
    print(f"Features: {X.shape[1]}")

    model = train_model(X)

    save_model(model)

    print("\nModel trained successfully.")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()