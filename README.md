# Phishing Detector

A Python-based phishing detection system using machine learning to analyze URLs and identify potential phishing threats.

## Objective

Analyze URLs and classify them as legitimate or potentially malicious using a trained Machine Learning model.

## Technologies

- Python
- Scikit-learn
- Pandas
- NumPy
- TLDExtract
- Joblib
- Pytest

## Project Structure

```text
phishing-detector/
├── data/
│   └── urls.csv
├── detector/
│   ├── __init__.py
│   ├── analyzer.py
│   └── predictor.py
├── model/
│   └── phishing_model.pkl
├── tests/
│   ├── test_analyzer.py
│   └── test_predictor.py
├── .gitignore
├── main.py
├── pytest.ini
├── README.md
├── requirements.txt
└── train.py
```

## Installation

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd phishing-detector
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Dataset

This project uses the **PhiUSIIL Phishing URL Dataset** from the UCI Machine Learning Repository.

- **Authors:** Arvind Prasad and Shalini Chandra.
- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/967/)
- **Publication:** Prasad, A., & Chandra, S. (2024). *PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning.*
- **DOI:** [10.1016/j.cose.2023.103545](https://doi.org/10.1016/j.cose.2023.103545)
- **License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**Modifications:** The original dataset is filtered, cleaned, and adapted for this project's URL-based phishing detection model. Only URL-related information and classification labels are retained.

**Classification:**

- `0` — Legitimate
- `1` — Phishing

## Machine Learning Model

The project uses a **Random Forest Classifier** implemented with Scikit-learn.

The model is trained using extracted URL features and saved as a serialized `.pkl` file using Joblib.

**Training configuration:**

- Algorithm: Random Forest
- Number of estimators: 100
- Test size: 20%
- Random state: 42
- Class weight: Balanced

Model training and evaluation are performed through `train.py`.

To train the model:

```bash
python train.py
```

The trained model is saved to:

```text
model/phishing_model.pkl
```

## Usage

Run the commands from the project root. The model must be trained first (`python train.py`).

Analyze a single URL:

```bash
python main.py https://www.google.com
```

Analyze multiple URLs:

```bash
python main.py https://www.google.com https://example.com
```

Interactive mode (type `q`, `quit`, or `exit` to leave):

```bash
python main.py
```

Example output:

```text
URL:        https://www.google.com
Prediction: Legitimate
Reason:     Trusted domain
```

The program exits with code `1` if any URL is invalid.

## URL Analyzer

The URL analyzer is responsible for validating URLs and extracting relevant features for the Machine Learning model.

It extracts 12 features, including:

- URL, domain, and path length
- Number of dots, hyphens, special characters, and digits
- Number of subdomains
- HTTPS usage
- IP address detection
- Suspicious words detection

These features are organized into a structured format that can be processed by the prediction system.

## Prediction System

The prediction system uses the trained Random Forest model to classify URLs.

The `predictor.py` module:

- Loads the trained model using Joblib.
- Extracts URL features through `analyzer.py`.
- Organizes the extracted features into a DataFrame.
- Predicts whether a URL is legitimate or potentially malicious.
- Calculates the model's estimated confidence for the predicted class.
- Skips the model for URLs from a small allowlist of trusted domains and suffixes (e.g., `edu.br`, `gov.br`), returning "Trusted domain" as the reason.
- Normalizes URLs by removing trailing slashes, so `site.com/` and `site.com` produce the same features.

## Testing

Run the test suite from the project root:

```bash
pytest
```

The tests cover URL validation, feature extraction, the trusted domain allowlist, and the prediction output structure.

## Limitations

- The model analyzes only the structure of the URL, not domain reputation or page content.
- A small allowlist of trusted domains and suffixes bypasses the model to reduce false positives.
- Results are estimates and must not be treated as a security guarantee.

## Roadmap

- [x] Project structure setup
- [x] Dataset preparation
- [x] Machine Learning model training
- [x] URL analyzer development
- [x] Prediction system implementation
- [x] Terminal interface integration
- [x] Testing and documentation

## Status

Completed.