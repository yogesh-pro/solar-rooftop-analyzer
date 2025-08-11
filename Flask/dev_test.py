#!/usr/bin/env python3
"""
Development Testing Script
Quick test to verify Flask app imports and basic functionality work
"""
import os
import sys

# Set API key
os.environ["OPENROUTER_API_KEY"] = "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"

try:
    print("🔍 Testing imports...")
    from model_loader import load_model_with_fallback
    print("✅ model_loader imported successfully")
    
    from main import app
    print("✅ main imported successfully")
    
    print("\nStarting Flask app on port 8080...")
    print("Open your browser and go to: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=8080)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
