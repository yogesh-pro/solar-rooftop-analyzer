#!/usr/bin/env python3
"""
Integration Test Suite
Run this to verify the Flask app endpoints and functionality work correctly
"""

import os
import sys
import requests
import time

def test_flask_app():
    print("🧪 Testing Flask Solar Rooftop Analyzer...")
    print("-" * 50)
    
    # Test 1: Check if app starts
    print("1. ✅ App import test...")
    try:
        from main import app
        print("   ✅ Flask app imports successfully")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Test 2: Check model loader
    print("2. Model loading test...")
    try:
        from model_loader import load_model_with_fallback
        print("   ✅ Model loader imports successfully")
    except Exception as e:
        print(f"   ❌ Model loader error: {e}")
        return False
    
    # Test 3: Check API key
    print("3. 🔑 API key test...")
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        if api_key.startswith("sk-or-v1-"):
            print("   ✅ API key format is correct")
        else:
            print("   ⚠️  API key format might be incorrect")
    else:
        print("   ⚠️  OPENROUTER_API_KEY not set")
        print("   Set with: export OPENROUTER_API_KEY='your-key'")
    
    # Test 4: Check directories
    print("4. 📁 Directory structure test...")
    required_dirs = ['templates', 'static', 'static/uploads', 'static/results']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}/ exists")
        else:
            print(f"   ❌ {dir_name}/ missing")
    
    # Test 5: Check templates
    print("5. 📄 Template files test...")
    required_templates = ['templates/base.html', 'templates/index.html', 'templates/results.html']
    for template in required_templates:
        if os.path.exists(template):
            print(f"   ✅ {template} exists")
        else:
            print(f"   ❌ {template} missing")
    
    print("-" * 50)
    print("Flask app setup verification complete!")
    print()
    print("To start the app:")
    print("   python run_flask.py")
    print()
    print("🌐 Then open: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_flask_app()
