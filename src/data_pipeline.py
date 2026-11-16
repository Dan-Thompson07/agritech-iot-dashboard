"""Data pipeline: ingest, validate, clean and classify farm sensor records.

Run from the repo root:  python src/data_pipeline.py
Writes a cleaned, alert-labelled CSV that the Power BI dashboard reads.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "sensor_telemetry_dataset.csv"
OUT_PATH = ROOT / "data" / "processed" / "farm_stress_alerts.csv"

MOISTURE_THRESHOLD = 20.0  # % soil moisture below which a farm is flagged
TEMPERATURE_THRESHOLD = 28.0  # deg C above which a dry farm becomes Critical

FLOAT_COLS = ["Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm", "Crop_Yield_ton"]
REQUIRED_COLS = FLOAT_COLS + ["Farm_ID", "Crop_Type", "Fertilizer_Usage_kg",
                              "Pesticide_Usage_kg", "Sustainability_Score"]


def validate(df: pd.DataFrame) -> None:
    """Fail loudly on structural problems; report data-quality checks."""
    missing = set(REQUIRED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    print(f"Null values: {int(df.isna().sum().sum())} | "
          f"Duplicate Farm_IDs: {int(df['Farm_ID'].duplicated().sum())}")


def classify_stress(df: pd.DataFrame) -> pd.Series:
    """Normal / Warning / Critical moisture-stress label (rule-based)."""
    dry = df["Soil_Moisture"] < MOISTURE_THRESHOLD
    hot = df["Temperature_C"] > TEMPERATURE_THRESHOLD
    return pd.Series(
        np.select([dry & hot, dry], ["Critical", "Warning"], default="Normal"),
        index=df.index,
        name="Stress_Level",
    )


def load_and_clean_data(filepath: Path = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    validate(df)
    df = df.drop_duplicates(subset="Farm_ID").dropna(subset=REQUIRED_COLS).copy()
    df[FLOAT_COLS] = df[FLOAT_COLS].round(2)
    df["Low_Moisture_Alert"] = df["Soil_Moisture"] < MOISTURE_THRESHOLD
    df["Stress_Level"] = classify_stress(df)
    return df


if __name__ == "__main__":
    data = load_and_clean_data()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUT_PATH, index=False)

    counts = data["Stress_Level"].value_counts()
    flagged = data["Low_Moisture_Alert"].mean() * 100
    print(f"Farms: {len(data):,}")
    print(counts.to_string())
    print(f"Flagged (Warning + Critical): {flagged:.1f}%")
    print(f"Saved -> {OUT_PATH.relative_to(ROOT)}")
