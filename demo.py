#!/usr/bin/env python3
"""
Demo script for the Stock Market Prediction Web App
"""

import webbrowser
import time
import subprocess
import sys
import os

def main():
    """Launch the web app and open browser"""

    print("🚀 Starting Stock Market Prediction Web App")
    print("=" * 50)

    # Check if required files exist
    required_files = ['app.py', 'index.html', 'best_random_forest.pkl', 'stockdata.csv']
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all files are in the current directory.")
        return

    print("✅ All required files found")

    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
        print("✅ Flask installed")

    # Start the Flask app
    print("🔥 Starting Flask server...")
    try:
        # Start Flask app in background
        process = subprocess.Popen([sys.executable, 'app.py'])

        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)

        # Open browser
        print("🌐 Opening web interface...")
        webbrowser.open('http://localhost:5000')

        print("\n" + "=" * 50)
        print("✅ Web app is running!")
        print("📱 Visit: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)

        # Keep the script running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            print("✅ Server stopped")

    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
