import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load the game log CSV
df = pd.read_csv('game_log.csv')

# --- Data Overview ---
# Assume columns like:
# ['game_id', 'move_number', 'row', 'col', 'adjacent_mines', 'hidden_neighbors', 
#  'flagged_neighbors', 'revealed_neighbors', 'label']

# Drop any rows with missing data
df.dropna(inplace=True)

# Convert categorical data (e.g., 'row', 'col') if necessary
# We'll treat 'row' and 'col' as numeric or one-hot, depending on model
# Option 1: Normalize row/col
df['row'] = df['row'] / df['row'].max()
df['col'] = df['col'] / df['col'].max()

# Option 2 (alternative): One-hot encode row and col if desired
# encoder = OneHotEncoder(sparse_output=False)
# encoded = encoder.fit_transform(df[['row', 'col']])
# encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(['row', 'col']))
# df = pd.concat([df.drop(['row', 'col'], axis=1), encoded_df], axis=1)

# Select feature columns
feature_cols = ['row', 'col', 'adjacent_mines', 'hidden_neighbors',
                'flagged_neighbors', 'revealed_neighbors']

X = df[feature_cols]
y = df['label']

# Train/test split for training the model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training data shape:", X_train.shape)
print("Test data shape:", X_test.shape)
