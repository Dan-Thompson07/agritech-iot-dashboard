import pandas as pd

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    
    float_cols = ['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm', 'Crop_Yield_ton']
    df[float_cols] = df[float_cols].round(2)
    
    df['Low_Moisture_Alert'] = df['Soil_Moisture'] < 20.0

    df['Stress_Level'] = 'Normal'
    df.loc[(df['Soil_Moisture'] < 20.0) & (df['Temperature_C'] > 28.0), 'Stress_Level'] = 'Critical'
    df.loc[(df['Soil_Moisture'] < 20.0) & (df['Temperature_C'] <= 28.0), 'Stress_Level'] = 'Warning'

    return df

if __name__ == "__main__":
    data_path = "data/sensor_telemetry_dataset.csv"
    data = load_and_clean_data(data_path)
    
    print("=== DATASET OVERVIEW ===")
    print(f"Total Rows: {len(data)}")
    print(f"Total Columns: {list(data.columns)}\n")
    
    print("=== SAMPLE RECORDS ===")
    print(data.head(5))
    
    print("\n=== STRESS LEVEL DISTRIBUTION ===")
    print(data['Stress_Level'].value_counts())