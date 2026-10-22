import pandas as pd


INPUT_PATH = "reports/anomaly_results.csv"
OUTPUT_PATH = "reports/anomaly_investigation.csv"


FEATURE_COLUMNS = [
    "failed_attempts",
    "successful_logins",
    "login_frequency",
    "unique_source_ips",
    "login_hour",
    "session_duration",
    "request_count"
]


def load_results():
    return pd.read_csv(INPUT_PATH)


def calculate_baselines(df):
    normal_events = df[df["is_anomaly"] == 0]

    baselines = {}

    for column in FEATURE_COLUMNS:
        baselines[column] = {
            "mean": normal_events[column].mean(),
            "std": normal_events[column].std()
        }

    return baselines


def explain_anomaly(row, baselines):
    reasons = []

    for feature in FEATURE_COLUMNS:
        mean = baselines[feature]["mean"]
        std = baselines[feature]["std"]

        if std == 0 or pd.isna(std):
            continue

        value = row[feature]

        z_score = abs(value - mean) / std

        if z_score >= 3:
            reasons.append(
                f"Extreme {feature.replace('_', ' ')}"
            )

        elif z_score >= 2:
            reasons.append(
                f"Unusual {feature.replace('_', ' ')}"
            )

    if not reasons:
        reasons.append("Combination of features differs from normal behavior")

    return reasons

def assign_priority(anomaly_score, score_quantiles):

    q25 = score_quantiles["q25"]
    q75 = score_quantiles["q75"]

    if anomaly_score <= q25:
        return "HIGH"

    elif anomaly_score <= q75:
        return "MEDIUM"

    return "LOW"


def analyze_anomalies(df):

    baselines = calculate_baselines(df)

    anomalies = df[df["is_anomaly"] == 1].copy()

    score_quantiles = {
        "q25": anomalies["anomaly_score"].quantile(0.25),
        "q75": anomalies["anomaly_score"].quantile(0.75)
    }

    explanations = []
    priorities = []

    for _, row in anomalies.iterrows():

        reasons = explain_anomaly(row, baselines)

        priority = assign_priority(
            row["anomaly_score"],
            score_quantiles
        )

        explanations.append("; ".join(reasons))
        priorities.append(priority)

    anomalies["reasons"] = explanations
    anomalies["priority"] = priorities

    return anomalies

def save_results(results):

    results.to_csv(
        OUTPUT_PATH,
        index=False
    )


def print_summary(results):

    print("\n=== ANOMALY INVESTIGATION SUMMARY ===")

    print(f"Anomalies analyzed: {len(results)}")

    priority_counts = results["priority"].value_counts()

    print(
        f"High Priority: "
        f"{priority_counts.get('HIGH', 0)}"
    )

    print(
        f"Medium Priority: "
        f"{priority_counts.get('MEDIUM', 0)}"
    )

    print(
        f"Low Priority: "
        f"{priority_counts.get('LOW', 0)}"
    )

    print("\n=== TOP ANOMALIES ===")

    top_anomalies = results.sort_values(
        "anomaly_score"
    ).head(10)

    for _, row in top_anomalies.iterrows():

        print(
            f"\nAnomaly Score: {row['anomaly_score']:.4f}"
        )

        print(
            f"Priority: {row['priority']}"
        )

        print(
            f"Reasons: {row['reasons']}"
        )


def main():

    print("=== ANOMALY INVESTIGATION ===")

    df = load_results()

    results = analyze_anomalies(df)

    save_results(results)

    print_summary(results)

    print(
        f"\nInvestigation results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()