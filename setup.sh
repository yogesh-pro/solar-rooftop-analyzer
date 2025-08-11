#!/bin/bash
# setup.sh - Quick setup script for Solar Rooftop Analyzer

echo "🚀 Setting up Solar Rooftop Analyzer with uv"
echo "=============================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
    echo "✅ uv installed successfully!"
fi

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate

# Install Flask dependencies
echo "Installing Flask application dependencies..."
uv pip install -e .

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Set up your OpenRouter API key in .env file"
echo "  3. Run the Flask app: cd Flask && python flask_app.py"
echo "  4. Open your browser to http://localhost:8080"
