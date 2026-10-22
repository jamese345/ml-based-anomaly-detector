import os
import unittest

import pandas as pd

from src.detect_anomalies import detect_anomalies
from src.analyze_anomalies import (
    calculate_baselines,
    explain_anomaly,
    assign_priority,
)
from src.generate_report import generate_report


class FakeModel:

    def predict(self, X):
        return [-1, 1, -1]

    def decision_function(self, X):
        return [-0.22, 0.05, -0.18]


class TestAnomalyDetector(unittest.TestCase):

    def setUp(self):

        self.df = pd.DataFrame({
            "failed_attempts": [20, 2, 15],
            "successful_logins": [1, 8, 2],
            "login_frequency": [15, 3, 12],
            "unique_source_ips": [8, 1, 6],
            "login_hour": [3, 14, 2],
            "session_duration": [500, 100, 450],
            "request_count": [300, 50, 250],
            "src_ip": [
                "10.0.0.1",
                "10.0.0.2",
                "10.0.0.3"
            ],
            "username": [
                "admin",
                "user",
                "test"
            ],
            "timestamp": [
                "2026-10-22 03:00:00",
                "2026-10-22 14:00:00",
                "2026-10-22 02:00:00"
            ]
        })


    def test_anomaly_detection(self):

        model = FakeModel()

        results = detect_anomalies(
            self.df,
            model
        )

        self.assertIn(
            "prediction",
            results.columns
        )

        self.assertIn(
            "anomaly_score",
            results.columns
        )

        self.assertIn(
            "is_anomaly",
            results.columns
        )

        self.assertEqual(
            results["is_anomaly"].sum(),
            2
        )


    def test_anomaly_score_created(self):

        model = FakeModel()

        results = detect_anomalies(
            self.df,
            model
        )

        self.assertEqual(
            len(results["anomaly_score"]),
            3
        )

        self.assertAlmostEqual(
            results.iloc[0]["anomaly_score"],
            -0.22
        )


    def test_baseline_calculation(self):

        results = self.df.copy()

        results["is_anomaly"] = [1, 0, 1]

        baselines = calculate_baselines(
            results
        )

        self.assertIn(
            "failed_attempts",
            baselines
        )

        self.assertIn(
            "mean",
            baselines["failed_attempts"]
        )

        self.assertIn(
            "std",
            baselines["failed_attempts"]
        )


    def test_explanation_generation(self):

        results = self.df.copy()

        results["is_anomaly"] = [1, 0, 1]

        baselines = calculate_baselines(
            results
        )

        reasons = explain_anomaly(
            results.iloc[0],
            baselines
        )

        self.assertIsInstance(
            reasons,
            list
        )

        self.assertGreater(
            len(reasons),
            0
        )


    def test_high_priority(self):

        priority = assign_priority(
            -0.20,
            {
                "q25": -0.177,
                "q75": -0.148
            }
        )

        self.assertEqual(
            priority,
            "HIGH"
        )


    def test_medium_priority(self):

        priority = assign_priority(
            -0.16,
            {
                "q25": -0.177,
                "q75": -0.148
            }
        )

        self.assertEqual(
            priority,
            "MEDIUM"
        )


    def test_low_priority(self):

        priority = assign_priority(
            -0.10,
            {
                "q25": -0.177,
                "q75": -0.148
            }
        )

        self.assertEqual(
            priority,
            "LOW"
        )


    def test_report_generation(self):

        df = pd.DataFrame({
            "anomaly_score": [-0.22],
            "priority": ["HIGH"],
            "reasons": [
                "Extreme failed attempts"
            ],
            "src_ip": ["10.0.0.1"],
            "username": ["admin"],
            "timestamp": [
                "2026-10-22 03:00:00"
            ]
        })

        report = generate_report(df)

        self.assertIn(
            "ML ANOMALY DETECTION",
            report
        )

        self.assertIn(
            "HIGH",
            report
        )

        self.assertIn(
            "Extreme failed attempts",
            report
        )


if __name__ == "__main__":
    unittest.main()