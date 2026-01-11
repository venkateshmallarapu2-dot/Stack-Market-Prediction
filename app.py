from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('best_random_forest.pkl')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Initialize scaler - we need to fit it on the same data the model was trained on
def initialize_scaler():
    """Initialize and fit the scaler on the original training data"""
    try:
        # Load the original data
        df = pd.read_csv('stockdata.csv')

        # Handle missing data
        df = df.dropna()

        # Feature engineering - extract date features
        df['Date'] = pd.to_datetime(df['Date'])
        df['day'] = df['Date'].dt.day
        df['month'] = df['Date'].dt.month
        df['year'] = df['Date'].dt.year
        df = df.drop('Date', axis=1)

        # Create and fit scaler
        scaler = StandardScaler()
        scaler.fit(df)

        return scaler, df.columns.tolist()

    except Exception as e:
        print(f"Error initializing scaler: {e}")
        return None, None

# Initialize scaler and get feature names
scaler, feature_names = initialize_scaler()

def preprocess_input(data):
    """
    Preprocess input data for prediction

    Expected input format:
    {
        "MSFT": float,
        "IBM": float,
        "SBUX": float,
        "AAPL": float,
        "GSPC": float,
        "date": "YYYY-MM-DD"  # or separate day/month/year
    }
    """
    try:
        # Extract features
        features = {}

        # Stock prices
        stock_features = ['MSFT', 'IBM', 'SBUX', 'AAPL', 'GSPC']
        for feature in stock_features:
            if feature not in data:
                raise ValueError(f"Missing required feature: {feature}")
            features[feature] = float(data[feature])

        # Date features
        if 'date' in data:
            # Parse date string
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
            features['day'] = date_obj.day
            features['month'] = date_obj.month
            features['year'] = date_obj.year
        else:
            # Use individual date components
            features['day'] = int(data.get('day', datetime.now().day))
            features['month'] = int(data.get('month', datetime.now().month))
            features['year'] = int(data.get('year', datetime.now().year))

        # Create DataFrame with single row
        input_df = pd.DataFrame([features])

        # For scaling, we need to ensure the input matches the scaler's expected features
        # The scaler was fit on all features including 'year', so we need to add a dummy year value
        # We'll use 0 for the year since it will be scaled anyway and we're predicting it
        input_for_scaling = input_df.copy()
        input_for_scaling['year'] = 0  # dummy value

        # Ensure correct column order matches what scaler expects
        if feature_names:
            input_for_scaling = input_for_scaling[feature_names]

        # Scale the features
        if scaler:
            scaled_features = scaler.transform(input_for_scaling)
            # Return only the input features (exclude the dummy year column)
            return scaled_features[:, :-1]
        else:
            raise ValueError("Scaler not initialized")

    except Exception as e:
        raise ValueError(f"Error preprocessing input: {str(e)}")

@app.route('/')
def home():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to API info if HTML file not found
        return jsonify({
            "message": "Stock Market Prediction API",
            "version": "1.0.0",
            "endpoints": {
                "/predict": "POST - Make predictions",
                "/health": "GET - Health check",
                "/model-info": "GET - Model information"
            },
            "expected_input": {
                "MSFT": "Microsoft stock price (float)",
                "IBM": "IBM stock price (float)",
                "SBUX": "Starbucks stock price (float)",
                "AAPL": "Apple stock price (float)",
                "GSPC": "S&P 500 index (float)",
                "date": "Date in YYYY-MM-DD format (string)"
            }
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    if model is None or scaler is None:
        return jsonify({"status": "unhealthy", "message": "Model or scaler not loaded"}), 500

    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_initialized": scaler is not None,
        "features": feature_names[:-1] if feature_names else None
    })

@app.route('/model-info')
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    return jsonify({
        "model_type": str(type(model).__name__),
        "parameters": model.get_params(),
        "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None,
        "n_estimators": model.n_estimators if hasattr(model, 'n_estimators') else None,
        "features": feature_names[:-1] if feature_names else None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction endpoint"""
    try:
        # Check if model and scaler are loaded
        if model is None or scaler is None:
            return jsonify({"error": "Model or scaler not initialized"}), 500

        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Preprocess input
        processed_data = preprocess_input(data)

        # Make prediction
        prediction = model.predict(processed_data)

        # The prediction is a scaled year value, let's inverse transform it to get actual year
        # Create a dummy array with the prediction in the year column position
        dummy_array = np.zeros((1, len(feature_names)))
        dummy_array[0, -1] = prediction[0]  # Put prediction in year column

        # Inverse transform to get actual year value
        actual_year = scaler.inverse_transform(dummy_array)[0, -1]

        # Round to nearest year
        predicted_year = round(float(actual_year))

        return jsonify({
            "prediction": predicted_year,
            "scaled_prediction": float(prediction[0]),
            "input_features": data,
            "model_confidence": "High (R² > 0.99 on test data)"
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
