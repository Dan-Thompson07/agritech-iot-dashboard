import pandas as pd

def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    """
    Loads IoT agricultural sensor telemetry and computes rolling statistics.
    """
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate rolling hourly mean for soil moisture per zone
    df['moisture_rolling_avg'] = (
        df.groupby('zone_id')['soil_moisture_pct']
        .transform(lambda x: x.rolling(window=2, min_periods=1).mean())
    )
    
    # Flag moisture deficit alerts (< 20%)
    df['irrigation_alert'] = df['soil_moisture_pct'] < 20.0
    
    return df

if __name__ == "__main__":
    data_path = "data/sensor_telemetry.csv"
    processed_df = load_and_preprocess_data(data_path)
    print("--- Processed Telemetry Sample ---")
    print(processed_df.head())
