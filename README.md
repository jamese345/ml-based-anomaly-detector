# 🧠 ML-Based Anomaly Detector

A Python-based Security Operations Center (SOC) machine learning system that analyzes security events, learns normal behavioral patterns, detects anomalous activity using **Isolation Forest**, explains unusual behavior, assigns investigation priorities, and generates SOC-focused reports and visualizations.

This project is part of my journey toward becoming an **AI SOC Analyst**, combining cybersecurity operations, Python automation, machine learning, and eventually AI-driven security analysis.

---

## 🎯 Project Goal

SOC environments generate large volumes of security events every day.

Traditional detection rules are effective for known patterns, but they may not identify unusual behavior that does not match a predefined rule.

This project explores how **unsupervised machine learning** can help identify potentially suspicious security activity by learning behavioral patterns and detecting events that significantly differ from normal activity.

The system automates the initial anomaly-analysis process by:

- Generating security event data
- Exploring security-event patterns
- Engineering behavioral features
- Training an Isolation Forest model
- Detecting anomalous events
- Calculating anomaly scores
- Comparing anomalous behavior against normal baselines
- Generating explanations for unusual behavior
- Assigning investigation priorities
- Generating a SOC visualization dashboard
- Producing an automated SOC investigation report
- Exporting machine-readable CSV results

The goal is to provide SOC analysts with an additional behavioral signal that can help identify events requiring further investigation.

---

## 🏗️ Architecture

```text
                    Security Events
                           │
                           ▼
                  security_events.csv
                           │
                           ▼
                   Data Exploration
                           │
                           ▼
                  Feature Engineering
                           │
                           ▼
                  Behavioral Features
                           │
                           ▼
                  Isolation Forest
                           │
                           ▼
                  Anomaly Detection
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
           Normal Events          Anomalies
                │                     │
                │                     ▼
                │             Anomaly Investigation
                │                     │
                │             ┌───────┴───────┐
                │             ▼               ▼
                │       Feature Analysis   Anomaly Score
                │             │               │
                │             └───────┬───────┘
                │                     ▼
                │              Priority Assignment
                │                     │
                │          ┌──────────┼──────────┐
                │          ▼          ▼          ▼
                │        HIGH       MEDIUM      LOW
                │
                └──────────────┬───────────────┘
                               ▼
                       SOC Visualization
                               │
                               ▼
                       SOC Investigation
                            Report
```

---

## 🔥 Key Features

### 1. Security Event Analysis

The project analyzes security-event data containing behavioral information such as:

- Failed authentication attempts
- Successful logins
- Login frequency
- Unique source IP addresses
- Login hour
- Session duration
- Request count

These features provide behavioral signals that can be used to identify unusual activity.

---

### 2. Feature Engineering

Raw security-event information is transformed into machine-learning-ready behavioral features.

The model uses:

| Feature | Description |
|---|---|
| `failed_attempts` | Number of failed authentication attempts |
| `successful_logins` | Number of successful logins |
| `login_frequency` | Frequency of login activity |
| `unique_source_ips` | Number of unique source IP addresses |
| `login_hour` | Hour when login activity occurred |
| `session_duration` | Duration of the session |
| `request_count` | Number of requests generated |

These features allow the model to identify behavioral patterns that differ from the learned baseline.

---

## 🤖 Machine Learning — Isolation Forest

The project uses the **Isolation Forest** algorithm for unsupervised anomaly detection.

Isolation Forest is well suited to this project because it can identify unusual observations without requiring manually labeled malicious-event data.

The model produces:

- Normal events
- Anomalous events
- Anomaly scores

Lower anomaly scores represent events that are more unusual according to the trained model.

The model is saved using Joblib:

```text
models/isolation_forest.joblib
```

---

## 🚨 Anomaly Detection

The detection pipeline analyzes the complete security-event dataset and assigns each event:

```text
prediction
anomaly_score
is_anomaly
```

Current result:

```text
Events analyzed:       1,050
Normal events:           997
Anomalous events:         53
Anomaly rate:           5.05%
```

The detection results are exported to:

```text
reports/anomaly_results.csv
```

---

## 🔎 Anomaly Investigation

Detected anomalies are passed through a second analysis layer.

The investigation system compares anomalous events against the behavioral baseline of normal events.

It identifies unusually large deviations in features such as:

- Failed attempts
- Login frequency
- Unique source IPs
- Login hour
- Session duration
- Request count

Example:

```text
Anomaly Score: -0.1971
Priority: HIGH

Reasons:
- Extreme failed attempts
- Extreme login frequency
- Extreme unique source IPs
- Extreme login hour
- Extreme session duration
- Extreme request count
```

This adds an explainability layer to the machine-learning output.

---

## 🎯 Investigation Priority

Detected anomalies are prioritized based on their anomaly-score distribution.

The system uses the distribution of detected anomalies to classify events into:

| Priority | Meaning |
|---|---|
| HIGH | Most unusual detected behavior |
| MEDIUM | Moderately unusual behavior |
| LOW | Least unusual detected behavior |

Current results:

| Priority | Events |
|---|---:|
| HIGH | 14 |
| MEDIUM | 26 |
| LOW | 13 |
| **Total** | **53** |

This helps analysts focus first on the most unusual events.

---

## 📊 Anomaly Score Analysis

The current anomaly-score distribution is:

| Metric | Score |
|---|---:|
| Minimum | -0.223948 |
| 25th Percentile | -0.177353 |
| Median | -0.158361 |
| 75th Percentile | -0.148492 |
| Maximum | -0.000468 |

The project uses these observed score distributions rather than arbitrary fixed thresholds to determine investigation priority.

---

## 📈 SOC Dashboard

The project generates a SOC-focused visualization dashboard containing:

- Total events analyzed
- Number of anomalies
- Anomaly rate
- Priority distribution
- Anomaly-score distribution
- Top 10 most anomalous events
- Normal vs anomalous feature averages

Generated dashboard:

```text
reports/anomaly_dashboard.png
```

The dashboard provides a quick visual overview of the machine-learning detection results.

---

## 📝 Automated SOC Investigation Report

The project generates an automated text-based SOC investigation report containing:

- Executive summary
- Detection statistics
- Anomaly rate
- Priority breakdown
- Top anomalous events
- Anomaly scores
- Investigation reasons
- Recommended SOC actions

Generated report:

```text
reports/anomaly_report.txt
```

Example SOC workflow:

```text
Detect anomaly
      ↓
Calculate anomaly score
      ↓
Identify unusual features
      ↓
Assign investigation priority
      ↓
Generate analyst context
      ↓
Recommend investigation
```

---

## 📊 Example Results

The current implementation analyzed:

```text
==================================================
       ML ANOMALY DETECTION — SOC RESULTS
==================================================

Events Analyzed:       1,050
Normal Events:           997
Anomalous Events:         53
Anomaly Rate:           5.05%

Priority Breakdown:
--------------------------------------------------
HIGH:                     14
MEDIUM:                   26
LOW:                      13
==================================================
```

One of the most anomalous events produced:

```text
Anomaly Score: -0.2239
Priority: HIGH

Reasons:
- Extreme failed attempts
- Extreme login frequency
- Extreme unique source IPs
- Extreme login hour
- Extreme session duration
- Extreme request count
```

---

## 📁 Project Structure

```text
ml-based-anomaly-detector/
│
├── data/
│   └── security_events.csv
│
├── models/
│   └── isolation_forest.joblib
│
├── reports/
│   ├── anomaly_results.csv
│   ├── anomaly_investigation.csv
│   ├── anomaly_dashboard.png
│   └── anomaly_report.txt
│
├── src/
│   ├── generate_dataset.py
│   ├── explore_data.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── detect_anomalies.py
│   ├── analyze_anomalies.py
│   ├── visualize_anomalies.py
│   └── generate_report.py
│
├── tests/
│   ├── __init__.py
│   └── test_anomaly_detector.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/jamese345/ml-based-anomaly-detector.git
cd ml-based-anomaly-detector
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Generate the security-event dataset

```bash
python src/generate_dataset.py
```

### Explore the dataset

```bash
python src/explore_data.py
```

### Engineer behavioral features

```bash
python src/feature_engineering.py
```

### Train the Isolation Forest model

```bash
python src/train_model.py
```

### Detect anomalies

```bash
python src/detect_anomalies.py
```

### Investigate anomalies

```bash
python src/analyze_anomalies.py
```

### Generate the SOC dashboard

```bash
python src/visualize_anomalies.py
```

### Generate the SOC investigation report

```bash
python src/generate_report.py
```

### Run the automated tests

```bash
python -m unittest discover tests
```

---

## 🧪 Testing

The project includes an automated test suite covering the core anomaly-detection and investigation functionality.

Current result:

```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.052s

OK
```

The test suite covers:

- Anomaly detection
- Anomaly score generation
- Baseline calculation
- Anomaly explanation
- HIGH priority classification
- MEDIUM priority classification
- LOW priority classification
- SOC report generation

---

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Isolation Forest
- Matplotlib
- Joblib
- unittest
- Machine learning
- SOC automation concepts
- Behavioral anomaly detection
- Explainable security analysis

---

## 🔐 Security Concepts Demonstrated

This project demonstrates practical understanding of:

- Security event analysis
- Behavioral anomaly detection
- Authentication monitoring
- Unsupervised machine learning
- Isolation Forest
- Anomaly scoring
- Feature engineering
- Security analytics
- SOC investigation workflows
- Alert prioritization
- Explainable security automation
- Automated SOC reporting
- Analyst decision support

---

## ⚠️ Limitations

This project is a learning and portfolio implementation.

An anomaly does **not** automatically mean malicious activity.

An unusual event may represent:

- Legitimate user behavior
- A rare but valid activity
- Automated processes
- Configuration changes
- Administrative activity
- Potential malicious behavior

Therefore, anomaly detection should be treated as an **investigation signal**, not a final security verdict.

In a production SOC environment, the anomaly detector would ideally be combined with additional security telemetry and context.

Potential sources include:

- SIEM events
- Endpoint telemetry
- Network telemetry
- Authentication logs
- Threat intelligence
- User/entity behavior analytics
- Detection rules
- Incident response data

---

## 🤖 Future AI Roadmap

This project intentionally begins with **machine-learning-based anomaly detection** before introducing more advanced AI capabilities.

Future versions can evolve toward an AI-assisted SOC investigation system.

```text
Current
   │
   ▼
Isolation Forest
   │
   ▼
Behavioral Anomaly Detection
   │
   ▼
Threat Intelligence
   │
   ▼
Machine Learning
   │
   ▼
LLM-Assisted Investigation
   │
   ▼
RAG Security Knowledge
   │
   ▼
Automated Investigation
   │
   ▼
AI SOC Analyst
```

Potential future capabilities include:

- Real-time anomaly detection
- SIEM integration
- Threat intelligence enrichment
- IP reputation analysis
- MITRE ATT&CK mapping
- Behavioral profiling
- False-positive prediction
- LLM-generated investigation summaries
- Natural-language security investigation
- RAG-based cybersecurity knowledge
- Automated investigation playbooks
- Alert correlation
- Incident-response recommendations
- Interactive SOC dashboard

The long-term goal is to evolve these projects into an intelligent **AI SOC Analyst platform** capable of assisting analysts throughout the security investigation lifecycle.

---

## 📈 Learning Progression

This project represents the third stage of my cybersecurity automation journey.

### Project 1

🛡️ **SOC Log Analyzer**

Focus:

```text
Python
+
Security Logs
+
Detection
+
Analysis
```

### Project 2

🚨 **Automated Alert Triage Engine**

Focus:

```text
Python
+
SOC Automation
+
Risk Scoring
+
Threat Intelligence
+
Alert Prioritization
```

### Project 3

🧠 **ML-Based Anomaly Detector**

Focus:

```text
Python
+
Machine Learning
+
Feature Engineering
+
Behavioral Analysis
+
Anomaly Detection
+
SOC Investigation
```

### Long-Term Goal

🤖 **AI SOC Analyst**

```text
Cybersecurity
+
Python
+
Automation
+
Machine Learning
+
Threat Intelligence
+
AI
```

---

## 👨‍💻 Author

I'm building practical cybersecurity projects while developing my skills in Python, security operations, automation, machine learning, and AI.

My long-term goal is to become an **AI SOC Analyst** focused on building intelligent systems for:

- Threat detection
- Alert triage
- Security automation
- Anomaly detection
- Incident investigation
- Analyst decision support

---

## ⭐ Project Status

**Status: COMPLETE ✅**

- 1,050 security events analyzed
- 997 normal events detected
- 53 anomalous events detected
- 14 HIGH-priority anomalies
- 26 MEDIUM-priority anomalies
- 13 LOW-priority anomalies
- Isolation Forest machine-learning model
- Explainable anomaly investigation
- Automated priority classification
- SOC visualization dashboard
- Automated SOC investigation report
- 8 automated tests
- 8 tests passing
- End-to-end ML anomaly-detection pipeline
- GitHub-ready documentation

---

## 📌 Why This Project Matters

This project demonstrates the ability to take a common SOC challenge — identifying unusual behavior in large volumes of security events — and build a Python-based machine-learning solution that produces actionable investigation signals.

Rather than stopping at model training, the project connects:

**Machine Learning → Detection → Explanation → Prioritization → Visualization → SOC Reporting**

This provides a foundation for the next stage of my journey toward building an **AI-powered SOC Analyst**.