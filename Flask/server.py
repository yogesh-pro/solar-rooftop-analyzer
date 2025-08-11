#!/usr/bin/env python3
"""
Solar Rooftop Analyzer - Production Server
Run this script to start the Flask web application server
"""

import os
import sys
from main import app

if __name__ == '__main__':
    # Set environment variables if not already set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY not found!")
        print("Please set it with: export OPENROUTER_API_KEY='your-api-key-here'")
        print("Or add it to your .env file")
        sys.exit(1)
    
    print("Starting Solar Rooftop Analyzer (Flask)...")
    print("Open your browser and go to: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=8080)
