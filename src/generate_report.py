import pandas as pd


INPUT_PATH = "reports/anomaly_investigation.csv"
OUTPUT_PATH = "reports/anomaly_report.txt"


def load_data():
    return pd.read_csv(INPUT_PATH)


def generate_report(df):

    total_anomalies = len(df)

    high_count = (df["priority"] == "HIGH").sum()
    medium_count = (df["priority"] == "MEDIUM").sum()
    low_count = (df["priority"] == "LOW").sum()

    total_events = total_anomalies

    anomaly_rate = (
        total_anomalies / 1050
    ) * 100

    report = []

    report.append("=" * 70)
    report.append(
        "ML ANOMALY DETECTION — SOC INVESTIGATION REPORT"
    )
    report.append("=" * 70)

    report.append("")
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 70)

    report.append(
        f"Events analyzed:       1050"
    )

    report.append(
        f"Normal events:         997"
    )

    report.append(
        f"Anomalous events:      {total_anomalies}"
    )

    report.append(
        f"Anomaly rate:          {anomaly_rate:.2f}%"
    )

    report.append("")

    report.append("PRIORITY BREAKDOWN")
    report.append("-" * 70)

    report.append(
        f"HIGH:                  {high_count}"
    )

    report.append(
        f"MEDIUM:                {medium_count}"
    )

    report.append(
        f"LOW:                   {low_count}"
    )

    report.append("")

    report.append("TOP ANOMALIES")
    report.append("-" * 70)

    top_anomalies = (
        df.sort_values("anomaly_score")
        .head(10)
    )

    for index, (_, row) in enumerate(
        top_anomalies.iterrows(),
        start=1
    ):

        report.append("")
        report.append(
            f"{index}. Anomaly Score: "
            f"{row['anomaly_score']:.4f}"
        )

        report.append(
            f"   Priority: {row['priority']}"
        )

        report.append(
            f"   Reasons: {row['reasons']}"
        )

        if "src_ip" in row.index:
            report.append(
                f"   Source IP: {row['src_ip']}"
            )

        if "username" in row.index:
            report.append(
                f"   Username: {row['username']}"
            )

        if "timestamp" in row.index:
            report.append(
                f"   Timestamp: {row['timestamp']}"
            )

    report.append("")

    report.append("RECOMMENDED SOC ACTION")
    report.append("-" * 70)

    report.append(
        "1. Investigate HIGH priority anomalies first."
    )

    report.append(
        "2. Review source IP and authentication activity."
    )

    report.append(
        "3. Examine unusual login frequency and failed attempts."
    )

    report.append(
        "4. Review session duration and request activity."
    )

    report.append(
        "5. Correlate suspicious events with other security logs."
    )

    report.append(
        "6. Escalate confirmed malicious activity for incident response."
    )

    report.append("")

    report.append("=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)

    return "\n".join(report)


def save_report(report):

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)


def main():

    print("=== SOC REPORT GENERATION ===")

    df = load_data()

    report = generate_report(df)

    save_report(report)

    print(
        f"Report saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()