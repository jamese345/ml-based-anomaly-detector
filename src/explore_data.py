import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = "data/security_events.csv"


def load_data():
    return pd.read_csv(DATA_PATH)


def show_dataset_overview(df):
    print("\n=== DATASET OVERVIEW ===")
    print(f"Total events: {len(df)}")
    print(f"Total features: {df.shape[1]}")

    print("\nClass distribution:")
    print(df["label"].value_counts())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDataset statistics:")
    print(df.describe())


def compare_behavior(df):
    print("\n=== NORMAL VS ANOMALOUS BEHAVIOR ===")

    comparison = df.groupby("label").mean(numeric_only=True)

    print(comparison)


def visualize_failed_attempts(df):
    plt.figure(figsize=(10, 6))

    plt.hist(
        df[df["label"] == 0]["failed_attempts"],
        bins=20,
        alpha=0.7,
        label="Normal"
    )

    plt.hist(
        df[df["label"] == 1]["failed_attempts"],
        bins=20,
        alpha=0.7,
        label="Anomalous"
    )

    plt.xlabel("Failed Attempts")
    plt.ylabel("Number of Events")
    plt.title("Failed Login Attempts: Normal vs Anomalous")
    plt.legend()
    plt.show()


def visualize_request_count(df):
    plt.figure(figsize=(10, 6))

    plt.hist(
        df[df["label"] == 0]["request_count"],
        bins=20,
        alpha=0.7,
        label="Normal"
    )

    plt.hist(
        df[df["label"] == 1]["request_count"],
        bins=20,
        alpha=0.7,
        label="Anomalous"
    )

    plt.xlabel("Request Count")
    plt.ylabel("Number of Events")
    plt.title("Request Count: Normal vs Anomalous")
    plt.legend()
    plt.show()


if __name__ == "__main__":

    df = load_data()

    show_dataset_overview(df)

    compare_behavior(df)

    visualize_failed_attempts(df)

    visualize_request_count(df)