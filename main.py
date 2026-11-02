import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "data" / "phiusiil_original.csv"

df = pd.read_csv(DATASET_PATH)

print(df.head())
print(df.columns)
print(df.shape)
print(df["label"].value_counts())
