import xgboost as xgb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def train_and_predict_recursive(df: pd.DataFrame, days_to_predict: int) -> float:
    """
    Trains XGBoost on data, then recursively predicts future days.
    """
    # 1. Prepare Data
    feature_cols = ['Open', 'High', 'Low', 'Volume', 'SMA_10', 'SMA_50', 'Daily_Return', 
                    'Close_Lag_1', 'Close_Lag_2', 'Close_Lag_3', 'Close_Lag_5']
    
    # Ensure we have all columns
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0 # Fallback
            
    X = df[feature_cols]
    y = df['Close']
    
    # 2. Train Model (Fast training)
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X, y)
    
    # 3. Recursive Prediction Loop
    # We take the last known row and use it to predict tomorrow, then use that to predict next day
    last_row = df.iloc[-1].copy()
    current_prediction = last_row['Close']
    
    for _ in range(days_to_predict):
        # Update lag features based on previous prediction
        last_row['Close_Lag_5'] = last_row['Close_Lag_3']
        last_row['Close_Lag_3'] = last_row['Close_Lag_2']
        last_row['Close_Lag_2'] = last_row['Close_Lag_1']
        last_row['Close_Lag_1'] = current_prediction
        
        # Prepare input for model
        input_data = pd.DataFrame([last_row[feature_cols]])
        
        # Predict
        current_prediction = model.predict(input_data)[0]
        
        # Update "last_row" features for next loop (Approximation logic)
        last_row['SMA_10'] = (last_row['SMA_10'] * 9 + current_prediction) / 10
        
    return float(current_prediction)