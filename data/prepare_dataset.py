import pandas as pd
from pathlib import Path
from urllib.parse import urlsplit

# File paths
DATA_DIR = Path(__file__).parent
INPUT_FILE = DATA_DIR / "phiusiil_original.csv"
OUTPUT_FILE = DATA_DIR / "phishing_dataset.csv"

def is_valid_url(url):
    try:
        parsed = urlsplit(url)
        return (
            parsed.scheme in ("http", "https")
            and parsed.hostname is not None
        )
    except ValueError:
        return False
    
def prepare_dataset():
    print("[+] Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    # Select only the required columns
    df = df[["URL", "label"]].copy()

    # Remove empty records
    df = df.dropna(subset=["URL", "label"])

    # Normalize spaces
    df["URL"] = df["URL"].astype(str).str.strip()

    # Convert labels to numbers
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])

    # Keep only known labels
    df = df[df["label"].isin([0, 1])]

    # Remove invalid URLs
    df = df[df["URL"].apply(is_valid_url)]

    # Remove URLs that appear with conflicting rankings
    conflicting = df.groupby("URL")["label"].nunique()
    conflicting_urls = conflicting[conflicting > 1].index
    df = df[~df["URL"].isin(conflicting_urls)]

    # Remove duplicates
    df = df.drop_duplicates(subset=["URL"])

    # Standardize classification:
    # 0 = legitimate | 1 = phishing
    df["label"] = df["label"].map({
        1: 0,
        0: 1
    }).astype(int)

    # Save prepared dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print("\n[+] Preparation completed!")
    print(f"[+] Total URLs: {len(df)}")
    print(f"[+] Legitimate: {(df['label'] == 0).sum()}")
    print(f"[+] Phishing: {(df['label'] == 1).sum()}")
    print(f"[+] File saved in: {OUTPUT_FILE}")

if __name__ == "__main__":
    prepare_dataset()
