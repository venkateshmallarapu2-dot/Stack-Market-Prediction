# Stock Market Prediction API

A Flask-based REST API for stock market year prediction using a trained RandomForest model.

## Features

- **Stock Price Prediction**: Predicts the year based on stock prices (MSFT, IBM, SBUX, AAPL, GSPC)
- **Date-based Features**: Automatically extracts day, month, and year features from input dates
- **Data Scaling**: Properly scales input data using the same scaler used during training
- **RESTful Endpoints**: Clean API endpoints for predictions and model information

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your model file `best_random_forest.pkl` and data file `stockdata.csv` are in the same directory as `app.py`.

## Quick Start

Run the demo script to automatically start the server and open your browser:

```bash
python demo.py
```

Or start manually:

```bash
python app.py
```

Then visit `http://localhost:5000` in your browser.

## Usage

### Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Access the Web Interface

Open your browser and navigate to `http://localhost:5000` to use the beautiful web interface, or use the API endpoints directly.

#### Web Interface Features

- **Modern UI**: Beautiful gradient design with responsive layout
- **Real-time Predictions**: Instant results with loading animations
- **Sample Data**: One-click loading of sample stock data
- **Error Handling**: Clear error messages and validation
- **Mobile Friendly**: Works perfectly on all devices

### API Endpoints

#### 1. Home - API Information
```
GET /
```
Returns API information and available endpoints.

#### 2. Health Check
```
GET /health
```
Returns the health status of the API and model.

#### 3. Model Information
```
GET /model-info
```
Returns information about the loaded model including parameters and features.

#### 4. Make Prediction
```
POST /predict
```

**Request Body:**
```json
{
    "MSFT": 23.950705,
    "IBM": 80.517962,
    "SBUX": 16.149666,
    "AAPL": 11.086612,
    "GSPC": 1416.599976,
    "date": "2007-01-03"
}
```

**Response:**
```json
{
    "prediction": 2007,
    "scaled_prediction": -1.5461474734420662,
    "input_features": {
        "MSFT": 23.950705,
        "IBM": 80.517962,
        "SBUX": 16.149666,
        "AAPL": 11.086612,
        "GSPC": 1416.599976,
        "date": "2007-01-03"
    },
    "model_confidence": "High (R² > 0.99 on test data)"
}
```

### Input Parameters

- `MSFT`: Microsoft stock price (float)
- `IBM`: IBM stock price (float)
- `SBUX`: Starbucks stock price (float)
- `AAPL`: Apple stock price (float)
- `GSPC`: S&P 500 index value (float)
- `date`: Date in YYYY-MM-DD format (string)

### Example Usage with Python

```python
import requests

# Test data
data = {
    "MSFT": 23.950705,
    "IBM": 80.517962,
    "SBUX": 16.149666,
    "AAPL": 11.086612,
    "GSPC": 1416.599976,
    "date": "2007-01-03"
}

# Make prediction
response = requests.post("http://localhost:5000/predict", json=data)
result = response.json()

print(f"Predicted year: {result['prediction']}")
```

### Example Usage with curl

```bash
curl -X POST "http://localhost:5000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "MSFT": 23.950705,
       "IBM": 80.517962,
       "SBUX": 16.149666,
       "AAPL": 11.086612,
       "GSPC": 1416.599976,
       "date": "2007-01-03"
     }'
```

## Model Details

- **Algorithm**: RandomForestRegressor
- **Training Data**: Historical stock prices from 2007 onwards
- **Features**: MSFT, IBM, SBUX, AAPL, GSPC stock prices + date features (day, month)
- **Target**: Year (predicted)
- **Performance**: R² > 0.99 on test data

## Error Handling

The API includes comprehensive error handling for:
- Missing required features
- Invalid data formats
- Model/scaler loading issues
- Unexpected errors

All errors return appropriate HTTP status codes and descriptive error messages.

## Production Deployment

For production deployment, consider:
- Using a production WSGI server (gunicorn, uWSGI)
- Adding authentication/authorization
- Implementing rate limiting
- Adding logging and monitoring
- Using environment variables for configuration
