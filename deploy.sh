#!/bin/bash

echo "🚀 Setting up Solar Rooftop Analyzer for Heroku deployment..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please log in to Heroku:"
    heroku login
fi

# Create Heroku app
echo "📝 Creating Heroku app..."
read -p "Enter your app name (or press Enter for auto-generated): " APP_NAME

if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create $APP_NAME
fi

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "⚠️  You'll need to set your OpenRouter API key manually in Heroku dashboard"
echo "   or use: heroku config:set OPENROUTER_API_KEY=your_api_key_here"

# Set buildpacks for better performance
echo "🏗️  Setting up buildpacks..."
heroku buildpacks:set heroku/python

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy solar rooftop analyzer to Heroku"
git push heroku main

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at: https://$(heroku apps:info --json | jq -r '.app.web_url')"
echo ""
echo "📋 Next steps:"
echo "1. Set your OpenRouter API key: heroku config:set OPENROUTER_API_KEY=your_key"
echo "2. Upload your model file to cloud storage and update model_loader.py"
echo "3. Test your deployment!"
