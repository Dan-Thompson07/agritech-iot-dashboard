import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_yield_predictor():
    # Dynamically find the path to sensor_telemetry_dataset.csv
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "sensor_telemetry_dataset.csv")
    
    # 1. Load data
    df = pd.read_csv(data_path)
    
    # 2. Define numerical feature variables (X)
    feature_cols = [
        'Soil_pH', 'Soil_Moisture', 'Temperature_C', 
        'Rainfall_mm', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg'
    ]
    X = df[feature_cols].copy()
    
    # One-Hot Encode categorical variable 'Crop_Type' if present
    if 'Crop_Type' in df.columns:
        crop_dummies = pd.get_dummies(df['Crop_Type'], prefix='Crop', drop_first=True)
        X = pd.concat([X, crop_dummies], axis=1)
        
    y = df['Crop_Yield_ton']
    
    # 3. Split data into 80% training set and 20% testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 4. Instantiate and train Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Make predictions and evaluate performance
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("=== MODEL TRAINING COMPLETE ===")
    print(f"Training set size: {len(X_train)} samples")
    print(f"Test set size: {len(X_test)} samples")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"R-squared Score (R²): {r2:.4f}")
    
    # Print Feature Importances
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\n=== FEATURE IMPORTANCE RANKING ===")
    print(importances.round(4))
    
    return model

if __name__ == "__main__":
    train_yield_predictor()