"""Exploratory yield model (Random Forest). Run from repo root: python src/model.py

Result: R^2 is approximately zero on the held-out set, i.e. the available features
do not predict Crop_Yield_ton. This is reported as a finding, not hidden.
"""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sensor_telemetry_dataset.csv"
FEATURES = ["Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
            "Fertilizer_Usage_kg", "Pesticide_Usage_kg"]


def train_yield_predictor():
    df = pd.read_csv(DATA_PATH)
    X = pd.concat([df[FEATURES], pd.get_dummies(df["Crop_Type"], prefix="Crop", drop_first=True)], axis=1)
    y = df["Crop_Yield_ton"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)
    pred = model.predict(X_test)
    baseline_mse = mean_squared_error(y_test, [y_train.mean()] * len(y_test))

    print(f"Train/test: {len(X_train)}/{len(X_test)}")
    print(f"MSE: {mean_squared_error(y_test, pred):.4f} (mean-baseline MSE: {baseline_mse:.4f})")
    print(f"R2:  {r2_score(y_test, pred):.4f}")
    print(pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False).round(4))
    return model


if __name__ == "__main__":
    train_yield_predictor()
