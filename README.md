# Phishing Detector

A Python-based phishing detection system using machine learning to analyze URLs.

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
phishing_detector/
├── data/
│   ├── prepare_dataset.py
│   └── phishing_dataset.csv
├── detector/
├── models/
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd phishing_detector
```

Create and activate the virtual environment:

```bash
python -m venv .venv
```

Windows (PowerShell):

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
- **Source:** https://archive.ics.uci.edu/dataset/967/
- **Publication:** Prasad, A., & Chandra, S. (2024). *PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning.*
- **DOI:** https://doi.org/10.1016/j.cose.2023.103545
- **License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**Modifications:** The original dataset is filtered, cleaned, and adapted for this project's URL-based phishing detection model. Only URL-related information and classification labels are retained.

**Classification:**
- `0` — Legitimate
- `1` — Phishing

## Roadmap

- [x] Project structure setup
- [x] Dataset preparation
- [ ] Machine Learning model training
- [ ] URL analyzer development
- [ ] Prediction system implementation
- [ ] Terminal interface integration
- [ ] Testing and documentation

## Status

In development — Stage 3: Machine Learning model training.