# 🚀 Heroku Deployment Guide

This guide will help you deploy your Solar Rooftop Analyzer to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your project is in a Git repository

## Step 1: Prepare Your Model File

Since GitHub/Heroku has file size limits, you need to host your model file externally:

### Option A: Google Drive
1. Upload `rooftop_best_model.pt` to Google Drive
2. Make it publicly accessible
3. Get the file ID from the shareable link
4. Update `model_loader.py` with the download URL:
   ```python
   "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID"
   ```

### Option B: Dropbox
1. Upload your model to Dropbox
2. Get a direct download link
3. Update `model_loader.py` with the URL

### Option C: Other Cloud Storage
- AWS S3, Google Cloud Storage, Azure Blob Storage
- Any public URL that serves the file directly

## Step 2: Set Up Environment Variables

Your OpenRouter API key should not be hardcoded. Create a `.env` file locally:

```env
OPENROUTER_API_KEY=your_api_key_here
```

## Step 3: Deploy to Heroku

### Automatic Deployment (Recommended)
```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment
```bash
# 1. Login to Heroku
heroku login

# 2. Create a new Heroku app
heroku create your-app-name

# 3. Set environment variables
heroku config:set OPENROUTER_API_KEY=your_api_key_here

# 4. Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Step 4: Update API Key in Code

Update `app.py` to use environment variables:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "your_fallback_key")
)
```

## Step 5: Monitor Your App

```bash
# View logs
heroku logs --tail

# Open your app
heroku open

# Check app status
heroku ps
```

## Troubleshooting

### Common Issues:

1. **Build Failed - Memory Issues**
   ```bash
   heroku config:set BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python.git
   ```

2. **App Timeout on Startup**
   - Model download might be taking too long
   - Consider using a smaller model or faster hosting

3. **Memory Limit Exceeded**
   - Upgrade to a paid Heroku plan
   - Or optimize your model size

4. **Port Issues**
   - Ensure your Procfile uses `$PORT`
   - Check server configuration in app.py

### Useful Commands:

```bash
# Restart your app
heroku restart

# Scale your app
heroku ps:scale web=1

# Check config vars
heroku config

# Run commands on Heroku
heroku run python -c "import torch; print(torch.__version__)"
```

## File Structure for Deployment

```
solar-rooftop-analyzer/
├── app.py                 # Main Streamlit app
├── model_loader.py        # Model loading logic
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku process file
├── runtime.txt           # Python version
├── deploy.sh             # Deployment script
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── .gitignore            # Git ignore file
```

## Cost Considerations

- **Free Tier**: Limited to 550-1000 dyno hours/month
- **Hobby Tier**: $7/month for always-on apps
- **Professional**: Starting at $25/month for production apps

## Security Best Practices

1. Never commit API keys to Git
2. Use environment variables for sensitive data
3. Enable Heroku's security features
4. Regular security updates

## Next Steps After Deployment

1. Set up custom domain (optional)
2. Configure SSL certificate
3. Set up monitoring and alerts
4. Implement CI/CD pipeline

---

## Quick Commands Reference

```bash
# Create and deploy
heroku create your-app-name
git push heroku main

# Set config
heroku config:set KEY=value

# View logs
heroku logs --tail

# Open app
heroku open
```

Need help? Check the [Heroku documentation](https://devcenter.heroku.com/) or contact support!
