import pandas as pd


DATA_PATH = "data/security_events.csv"


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


def create_features(df):
    X = df[FEATURE_COLUMNS].copy()

    return X


def main():
    df = load_data()

    X = create_features(df)

    print("=== FEATURE ENGINEERING ===")

    print("\nSelected features:")
    for feature in X.columns:
        print(f"- {feature}")

    print(f"\nFeature matrix shape: {X.shape}")

    print("\nFeature matrix preview:")
    print(X.head())


if __name__ == "__main__":
    main()