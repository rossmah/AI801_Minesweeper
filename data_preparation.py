import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data():
    # Load the game log CSV
    df = pd.read_csv('game_data.csv')

    # Drop any rows with missing data
    df = df.dropna()

    # Feature selection
    features = ['Row', 'Col', 'Mines Flagged', 'Hidden Cells', 'Move Number']

    # Convert 'Safe' to binary labels (0 = mine, 1 = safe)
    df['Safe'] = df['Safe'].astype(int)

    x_raw = df[features]
    y = df['Safe']

    # Normalize features
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_raw)

    # Split into train/test 
    x_train, x_test, y_train, y_test = train_test_split(
        x_scaled, y, test_size=0.2, random_state=42
    )

    print("Training data shape:", x_train.shape)
    print("Test data shape:", x_test.shape)

    # 1. Check label distribution
    print("Column Names:")
    print(df.columns)

    print("Label distribution (Safe):")
    print(df['Safe'].value_counts(normalize=True))

    # 2. Check correlation of numeric features with 'Safe'
    numeric_cols = ['Row', 'Col', 'Mines Flagged', 'Hidden Cells', 'Move Number']
    if 'Move Number' in df.columns:
        df['Move Number'] = pd.to_numeric(df['Move Number'], errors='coerce')
        numeric_cols.append('Move Number')

    correlations = df[numeric_cols + ['Safe']].corr()

    # 3. Check for leakage from 'Action' and 'Game Outcome'
    print("\nSample values for Action and Game Outcome:")
    print(df[['Action', 'Game Outcome']].drop_duplicates().head())

    return x_train, x_test, y_train, y_test, scaler