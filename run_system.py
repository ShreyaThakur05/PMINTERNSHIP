#!/usr/bin/env python3
"""
Main runner script for the AI-Powered Internship Allocation System
"""

import subprocess
import sys
import os
import webbrowser
import time

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def generate_sample_data():
    """Generate sample data using the existing script"""
    print("Generating sample data...")
    subprocess.run([sys.executable, "datasetcode.py"])

def start_api_server():
    """Start the Flask API server"""
    print("Starting API server...")
    subprocess.Popen([sys.executable, "app.py"])

def open_frontend():
    """Open the frontend in browser"""
    time.sleep(3)  # Wait for server to start
    frontend_path = os.path.abspath("frontend.html")
    webbrowser.open(f"file://{frontend_path}")

def main():
    print("🎓 AI-Powered Internship Allocation System")
    print("=" * 50)
    
    try:
        # Step 1: Install requirements
        install_requirements()
        
        # Step 2: Generate sample data
        generate_sample_data()
        
        # Step 3: Start API server
        start_api_server()
        
        # Step 4: Open frontend
        print("Opening frontend in browser...")
        open_frontend()
        
        print("\n✅ System started successfully!")
        print("📊 Frontend: Open frontend.html in your browser")
        print("🔗 API Server: http://localhost:5000")
        print("\nNext steps:")
        print("1. Update .env file with your MongoDB Atlas connection string")
        print("2. Click 'Load Data from CSV' in the frontend")
        print("3. Click 'Run Allocation' to see the AI allocation in action")
        print("\nPress Ctrl+C to stop the system")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 System stopped")
            
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()