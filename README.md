
📈 Stock Market Prediction System Using Random Forest
1. Project Title
Stock Market Prediction Using Machine Learning and Flask API
2. Problem Statement
Stock market prices are highly volatile and depend on multiple factors such as company performance, market trends, and investor sentiment. Manual analysis is complex and time-consuming.
This project aims to build an AI-based stock prediction system that can forecast future stock prices using historical data and machine learning.
3. Objectives
To analyze historical stock price data
To train a machine learning model for prediction
To predict future closing prices
To deploy the model using Flask API
To provide a web-based interface for users
4. Dataset Description
The dataset contains historical stock prices of the following companies and indices:
Symbol
Company / Index
MSFT
Microsoft
IBM
IBM
USVX
Volatility Index
AAPL
Apple
GSPC
S&P 500 Index
Each dataset contains:
Date
Open price
High price
Low price
Close price
Volume
These values represent daily trading data.
5. Data Preprocessing
The following steps were applied:
Handling missing values
Removing unnecessary columns
Date conversion
Feature scaling
Creating input (X) and target (Y) variables
Splitting data into training and testing sets
6. Machine Learning Model
Random Forest Regressor
Random Forest is an ensemble learning technique that combines multiple decision trees to improve accuracy and avoid overfitting.
It was selected because:
It handles large datasets well
It works well with non-linear data
It reduces variance and improves prediction accuracy
7. Model Training Process
Stock data loaded
Features such as Open, High, Low, and Volume used as inputs
Close price used as output
Model trained using historical data
Performance evaluated using:
Mean Absolute Error (MAE)
Root Mean Square Error (RMSE)
R² Score
8. System Architecture
Copy code

User (Browser)
     |
HTML + CSS + JavaScript (Frontend)
     |
Flask API (Backend)
     |
Random Forest Model
     |
Prediction Result
     |
Displayed on Web Page
9. Frontend
Technologies used:
HTML – Structure
CSS – Styling
JavaScript – Data handling and API calls
User enters:
Stock name
Open, High, Low, Volume
The prediction is shown on the screen.
10. Backend – Flask API
Flask acts as the bridge between frontend and machine learning model.
Functions:
Receives user input
Loads trained Random Forest model
Predicts stock price
Sends result back to frontend
11. Deployment
The model is deployed using:
Flask REST API
HTML, CSS, JavaScript for UI
The user interacts through the browser and gets real-time predictions.
12. Advantages
High prediction accuracy
Easy-to-use web interface
Real-time predictions
Supports multiple stocks
13. Applications
Stock traders
Investment firms
Financial analysis platforms
Educational purposes
14. Conclusion
This project successfully predicts stock prices using Random Forest and historical market data. The Flask-based deployment allows users to access predictions through a web interface, making the system practical and user-friendly.
