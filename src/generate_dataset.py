import os
import numpy as np
import pandas as pd


def generate_normal_events(count=1000):
    np.random.seed(42)

    data = {
        "failed_attempts": np.random.poisson(1, count),
        "successful_logins": np.random.poisson(3, count),
        "login_frequency": np.random.normal(5, 1.5, count),
        "unique_source_ips": np.random.poisson(1, count) + 1,
        "login_hour": np.random.normal(10, 2.5, count),
        "session_duration": np.random.normal(30, 8, count),
        "request_count": np.random.normal(100, 25, count),
        "label": 0,
    }

    return pd.DataFrame(data)


def generate_anomalous_events(count=50):
    np.random.seed(99)

    data = {
        "failed_attempts": np.random.randint(15, 50, count),
        "successful_logins": np.random.randint(0, 2, count),
        "login_frequency": np.random.uniform(20, 50, count),
        "unique_source_ips": np.random.randint(5, 15, count),
        "login_hour": np.random.choice([1, 2, 3, 23], count),
        "session_duration": np.random.uniform(1, 5, count),
        "request_count": np.random.uniform(500, 1000, count),
        "label": 1,
    }

    return pd.DataFrame(data)


def generate_dataset():
    normal = generate_normal_events()
    anomalous = generate_anomalous_events()

    dataset = pd.concat([normal, anomalous], ignore_index=True)

    dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

    return dataset


if __name__ == "__main__":
    dataset = generate_dataset()

    # Define directory and ensure it exists safely
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # Save dataset safely
    output_path = os.path.join(output_dir, "security_events.csv")
    dataset.to_csv(output_path, index=False)

    print("Security dataset generated successfully.")
    print(f"Total events: {len(dataset)}")
    print(f"Normal events: {(dataset['label'] == 0).sum()}")
    print(f"Anomalous events: {(dataset['label'] == 1).sum()}")
