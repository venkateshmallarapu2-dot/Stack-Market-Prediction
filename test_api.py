#!/usr/bin/env python3
"""
Test script for the Stock Market Prediction API
"""

import requests
import json
import pandas as pd

def test_api():
    """Test all API endpoints"""

    base_url = "http://localhost:5000"

    print("Testing Stock Market Prediction API")
    print("=" * 40)

    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

    # Test 2: Home endpoint
    print("\n2. Testing Home endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Home endpoint working")
        else:
            print(f"❌ Home endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Home endpoint error: {e}")

    # Test 3: Model Info
    print("\n3. Testing Model Info...")
    try:
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            print("✅ Model info retrieved")
            data = response.json()
            print(f"   Model type: {data['model_type']}")
            print(f"   Number of features: {data['n_features']}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model info error: {e}")

    # Test 4: Prediction
    print("\n4. Testing Prediction...")

    # Load sample data from CSV
    try:
        df = pd.read_csv('stockdata.csv')
        sample = df.iloc[0]  # First row

        test_data = {
            "MSFT": float(sample['MSFT']),
            "IBM": float(sample['IBM']),
            "SBUX": float(sample['SBUX']),
            "AAPL": float(sample['AAPL']),
            "GSPC": float(sample['GSPC']),
            "date": sample['Date']
        }

        print(f"   Using test data from: {sample['Date']}")

        response = requests.post(f"{base_url}/predict", json=test_data)

        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"   Predicted year: {result['prediction']}")
            print(f"   Scaled prediction: {result['scaled_prediction']:.4f}")
            print(f"   Model confidence: {result['model_confidence']}")
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")

    except Exception as e:
        print(f"❌ Prediction error: {e}")

    # Test 5: Error handling
    print("\n5. Testing Error Handling...")
    try:
        # Test with missing features
        incomplete_data = {"MSFT": 100.0}  # Missing required features
        response = requests.post(f"{base_url}/predict", json=incomplete_data)

        if response.status_code == 400:
            print("✅ Error handling working - correctly rejected incomplete data")
        else:
            print(f"❌ Error handling failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Error handling test error: {e}")

    print("\n" + "=" * 40)
    print("API Testing Complete!")

if __name__ == "__main__":
    # Check if Flask app is running
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Flask app is not running!")
        print("Please start the Flask app first with: python app.py")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the Flask app is running on http://localhost:5000")
