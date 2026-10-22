import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = "reports/anomaly_investigation.csv"
OUTPUT_PATH = "reports/anomaly_dashboard.png"


def load_data():
    return pd.read_csv(INPUT_PATH)


def create_dashboard(df):

    total_events = len(pd.read_csv("reports/anomaly_results.csv"))
    anomaly_count = len(df)
    high_count = (df["priority"] == "HIGH").sum()
    medium_count = (df["priority"] == "MEDIUM").sum()
    low_count = (df["priority"] == "LOW").sum()

    anomaly_percentage = (anomaly_count / total_events) * 100

    fig = plt.figure(figsize=(14, 9))

    fig.suptitle(
        "ML-Based Anomaly Detection — SOC Dashboard",
        fontsize=18,
        fontweight="bold"
    )

    # ---------------------------------------------------------
    # 1. Summary
    # ---------------------------------------------------------

    ax1 = plt.subplot2grid((3, 2), (0, 0))

    ax1.axis("off")

    summary = (
        f"TOTAL EVENTS\n{total_events}\n\n"
        f"ANOMALIES\n{anomaly_count}\n\n"
        f"ANOMALY RATE\n{anomaly_percentage:.2f}%"
    )

    ax1.text(
        0.5,
        0.5,
        summary,
        ha="center",
        va="center",
        fontsize=14
    )

    # ---------------------------------------------------------
    # 2. Priority distribution
    # ---------------------------------------------------------

    ax2 = plt.subplot2grid((3, 2), (0, 1))

    priorities = ["HIGH", "MEDIUM", "LOW"]
    counts = [high_count, medium_count, low_count]

    ax2.bar(priorities, counts)

    ax2.set_title("Anomaly Priority Distribution")
    ax2.set_ylabel("Number of Anomalies")

    for i, count in enumerate(counts):
        ax2.text(
            i,
            count + 0.5,
            str(count),
            ha="center"
        )

    # ---------------------------------------------------------
    # 3. Anomaly score distribution
    # ---------------------------------------------------------

    ax3 = plt.subplot2grid((3, 2), (1, 0))

    ax3.hist(
        df["anomaly_score"],
        bins=12
    )

    ax3.set_title("Anomaly Score Distribution")
    ax3.set_xlabel("Isolation Forest Score")
    ax3.set_ylabel("Number of Events")

    # ---------------------------------------------------------
    # 4. Top anomalies
    # ---------------------------------------------------------

    ax4 = plt.subplot2grid((3, 2), (1, 1))

    top_anomalies = (
        df.sort_values("anomaly_score")
        .head(10)
        .copy()
    )

    top_anomalies["label"] = (
        top_anomalies.index.astype(str)
    )

    ax4.barh(
        top_anomalies["label"],
        top_anomalies["anomaly_score"]
    )

    ax4.set_title("Top 10 Most Anomalous Events")
    ax4.set_xlabel("Anomaly Score")

    # Most anomalous at top
    ax4.invert_yaxis()

    # ---------------------------------------------------------
    # 5. Feature comparison
    # ---------------------------------------------------------

    ax5 = plt.subplot2grid((3, 2), (2, 0), colspan=2)

    features = [
        "failed_attempts",
        "successful_logins",
        "login_frequency",
        "unique_source_ips",
        "session_duration",
        "request_count"
    ]

    normal_data = pd.read_csv(
        "reports/anomaly_results.csv"
    )

    normal_data = normal_data[
        normal_data["is_anomaly"] == 0
    ]

    anomaly_means = df[features].mean()
    normal_means = normal_data[features].mean()

    x = range(len(features))

    width = 0.35

    ax5.bar(
        [i - width / 2 for i in x],
        normal_means,
        width,
        label="Normal"
    )

    ax5.bar(
        [i + width / 2 for i in x],
        anomaly_means,
        width,
        label="Anomalous"
    )

    ax5.set_title(
        "Normal vs Anomalous Feature Averages"
    )

    ax5.set_ylabel("Average Value")

    ax5.set_xticks(list(x))
    ax5.set_xticklabels(
        features,
        rotation=30,
        ha="right"
    )

    ax5.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


def main():

    print("=== SOC ANOMALY DASHBOARD ===")

    df = load_data()

    create_dashboard(df)

    print(
        f"Dashboard saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()