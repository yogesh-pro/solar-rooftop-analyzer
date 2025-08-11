#!/bin/bash
# run-flask.sh - Run Flask application with uv

echo "🚀 Starting Flask Application"
echo "============================="

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ] && [ ! -f ".env" ]; then
    echo "⚠️  Warning: OPENROUTER_API_KEY not found in environment or .env file"
    echo "   Please set it up before running the application"
fi

# Navigate to Flask directory and run
cd Flask
echo "📍 Starting Flask app at http://localhost:8080"
python flask_app.py
