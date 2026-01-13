​1. Project Overview
​This project uses a Random Forest machine learning model to predict stock price movements based on historical data. It is deployed as a web application with a Flask API backend and a responsive HTML/CSS/JS frontend.
​Dataset Components
​The dataset includes historical price data (Open, High, Low, Close, Volume) for the following tickers:
​MSFT: Microsoft Corporation
​IBM: International Business Machines
​AAPL: Apple Inc.
​GSPC: S&P 500 Index (Market Benchmark)
​USVX: Volatility Index (Often used as a market "fear gauge")
​2. Machine Learning Model: Random Forest
​The Random Forest algorithm was chosen for its ability to handle non-linear relationships and its robustness against overfitting.
​Type: Ensemble Learning (Bagging).
​Process: It constructs multiple decision trees during training and outputs the mean prediction (regression) or the majority vote (classification) of the individual trees.
​Features: Includes technical indicators like Moving Averages (SMA/EMA), Relative Strength Index (RSI), and lagged price data.
​3. Backend Deployment: Flask API
​The Flask framework acts as the bridge between the trained Python model and the web interface.
​app.py Logic
​Load Model: The pre-trained Random Forest model is loaded using pickle or joblib.
​API Endpoint: A @app.route('/predict', methods=['POST']) receives JSON data from the frontend.
​Pre-processing: User input is converted into a format (NumPy array) the model understands.
​Inference: model.predict(data) generates the result.
​Response: The prediction is returned as a JSON object.
4. Frontend: HTML, CSS, & JavaScript
​The frontend provides a user-friendly interface to interact with the model.
​HTML: Creates the structure (input fields for stock features, buttons, and a result display area).
​CSS: Styles the dashboard for a professional, "fintech" look (dark mode, clean typography).
​JavaScript (Fetch API): Captures user input and sends an asynchronous request to the Flask /predict endpoint without refreshing the page.
5. System Architecture

​User enters data into the HTML/CSS UI.
​JavaScript sends a POST request to the Flask API.
​Flask runs the data through the Random Forest Model.
​The Result is sent back to the UI and displayed to the user.