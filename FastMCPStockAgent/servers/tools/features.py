import pandas as pd
import numpy as np

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Adds RSI, SMA, and Lag features for ML."""
    df = df.copy()
    
    # Simple Moving Averages
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # Returns
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Lag features (Values from previous days used to predict today)
    for lag in [1, 2, 3, 5]:
        df[f'Close_Lag_{lag}'] = df['Close'].shift(lag)
        
    df.dropna(inplace=True) # ML models don't like NaNs
    return df