#!/usr/bin/env python

import os
import subprocess
import sys
from dotenv import load_dotenv
from config.config import Config

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import streamlit
        import openai
        import pandas
        print("✅ All required dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install all required dependencies using: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if the OpenAI API key is set."""
    if not Config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY is not set in the .env file.")
        print("Please create a .env file with your OpenAI API key.")
        print("Example: OPENAI_API_KEY=your_api_key_here")
        return False
    else:
        print("✅ OpenAI API key is set.")
        return True

def create_data_directory():
    """Create the data directory if it doesn't exist."""
    if not os.path.exists(Config.DATA_DIR):
        os.makedirs(Config.DATA_DIR)
        print(f"✅ Created data directory: {Config.DATA_DIR}")
    else:
        print(f"✅ Data directory exists: {Config.DATA_DIR}")

def run_app():
    """Run the Streamlit application."""
    print(f"\n🚀 Starting {Config.APP_NAME}...\n")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

def main():
    """Main function to run the application."""
    print(f"\n=== {Config.APP_NAME} ===\n")
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check API key
    if not check_api_key():
        return
    
    # Create data directory
    create_data_directory()
    
    # Validate configuration
    is_valid, error_message = Config.validate_config()
    if not is_valid:
        print(f"❌ Configuration error: {error_message}")
        return
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()
