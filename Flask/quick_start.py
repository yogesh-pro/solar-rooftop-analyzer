#!/usr/bin/env python3
"""
Quick Start Script
Simple script to quickly start the Flask application with hardcoded API key for testing
"""
import os
import sys

def main():
    # Set API key
    os.environ["OPENROUTER_API_KEY"] = "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"
    
    try:
        print("🔍 Importing Flask app...")
        from main import app
        
        print("✅ Flask app imported successfully!")
        print()
        print("Starting Solar Rooftop Analyzer (Flask)")
        print("Open your browser and go to: http://localhost:8080")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the Flask development server
        app.run(
            debug=True,           # Enable debug mode for development
            host='0.0.0.0',      # Listen on all interfaces
            port=8080,           # Use port 8080 instead of 5000
            use_reloader=False   # Disable auto-reloader to prevent issues
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("🔧 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
