#!/usr/bin/env python3
"""
Pre-deployment test script for Solar Rooftop Analyzer
Run this script to verify everything is ready for Heroku deployment
"""

import sys
import os
import importlib.util
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_import(module_name):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False

def check_environment_variables():
    """Check environment variables"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        print(f"✅ OPENROUTER_API_KEY - Set (length: {len(api_key)})")
        return True
    else:
        print("⚠️  OPENROUTER_API_KEY - Not set (will use fallback)")
        return False

def main():
    print("🔍 Pre-deployment checks for Solar Rooftop Analyzer\n")
    
    all_good = True
    
    # Check required files
    print("📁 Checking required files:")
    required_files = [
        ("app.py", "Main application"),
        ("requirements.txt", "Dependencies"),
        ("Procfile", "Heroku process file"),
        ("runtime.txt", "Python version"),
        ("model_loader.py", "Model loader"),
        (".streamlit/config.toml", "Streamlit config"),
        ("DEPLOYMENT.md", "Deployment guide"),
    ]
    
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\n📦 Checking Python imports:")
    required_modules = [
        "streamlit", "torch", "torchvision", "PIL", 
        "numpy", "matplotlib", "requests", "openai"
    ]
    
    for module in required_modules:
        if not check_import(module):
            all_good = False
    
    print("\n🔧 Checking environment:")
    check_environment_variables()
    
    print(f"\n🐍 Python version: {sys.version}")
    
    # Check if git is initialized
    if Path(".git").exists():
        print("✅ Git repository - Initialized")
    else:
        print("❌ Git repository - Not initialized")
        all_good = False
    
    # Summary
    print("\n" + "="*50)
    if all_good:
        print("🚀 Ready for deployment!")
        print("\nNext steps:")
        print("1. Upload your model file to cloud storage")
        print("2. Update model URL in model_loader.py")
        print("3. Run: ./deploy.sh")
    else:
        print("⚠️  Some issues found. Please fix them before deploying.")
        print("\nRun 'pip install -r requirements.txt' to install dependencies")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
