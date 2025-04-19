import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load preprocessed data
df = pd.read_csv('data/processed_move_data.csv')

# Features and label
feature_cols = ['adjacent_mines', 'is_revealed', 'is_flagged', 'is_mine', 'row', 'col']
X = df[feature_cols]
y = df['label']  # 0 = safe, 1 = mine

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, 'models/minesweeper_model.pkl')
