import joblib
from sklearn.ensemble import RandomForestClassifier
from data_preparation import load_and_preprocess_data

def train_and_save_model():
    x_train, x_test, y_train, y_test, scaler = load_and_preprocess_data()

    # Initialize model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train classifier
    model.fit(x_train, y_train)

    # Evaluate
    score = model.score(x_test, y_test)
    print(f"Model accuracy: {score:.2f}")

    # Save model and scaler separately
    joblib.dump(model, 'models/model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    print(f"Model and scaler saved separately to models/")

if __name__ == "__main__":
    train_and_save_model()
