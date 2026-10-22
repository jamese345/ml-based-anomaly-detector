import pandas as pd
import joblib


DATA_PATH = "data/security_events.csv"
MODEL_PATH = "models/isolation_forest.joblib"
OUTPUT_PATH = "reports/anomaly_results.csv"


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


def load_model():
    return joblib.load(MODEL_PATH)


def detect_anomalies(df, model):
    X = df[FEATURE_COLUMNS]

    predictions = model.predict(X)
    scores = model.decision_function(X)

    results = df.copy()

    results["prediction"] = predictions
    results["anomaly_score"] = scores

    results["is_anomaly"] = results["prediction"].apply(
        lambda value: 1 if value == -1 else 0
    )

    return results


def save_results(results):
    results.to_csv(
        OUTPUT_PATH,
        index=False
    )


def main():
    print("=== ANOMALY DETECTION ===")

    df = load_data()

    print(f"Events analyzed: {len(df)}")

    model = load_model()

    results = detect_anomalies(df, model)

    anomaly_count = results["is_anomaly"].sum()
    normal_count = len(results) - anomaly_count

    print(f"Normal events detected: {normal_count}")
    print(f"Anomalous events detected: {anomaly_count}")

    save_results(results)

    print(f"\nResults saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()