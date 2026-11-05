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
├── .gitignore
├── main.py
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

## Roadmap

- [x] Project structure setup
- [x] Dataset preparation
- [x] Machine Learning model training
- [x] URL analyzer development
- [ ] Prediction system implementation
- [ ] Terminal interface integration
- [ ] Testing and documentation

## Status

In development — Prediction system implementation.