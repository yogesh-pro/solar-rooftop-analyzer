# 🚀 Manual Heroku Deployment Steps

## Step 1: Install Heroku CLI (if not done)
```bash
# macOS with Homebrew
brew install heroku/brew/heroku

# Verify installation
heroku --version
```

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Create Heroku App
```bash
# Create with auto-generated name
heroku create

# Or create with specific name
heroku create your-solar-analyzer-app
```

## Step 4: Set Environment Variables
```bash
heroku config:set OPENROUTER_API_KEY=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
```

## Step 5: Upload Model to GitHub Release
1. Go to your GitHub repository: https://github.com/yogesh-pro/solar-rooftop-analyzer
2. Click "Releases" → "Create a new release"
3. Tag version: `Model` or `v1.0`
4. Title: "Model Release"
5. Upload your `rooftop_best_model.pt` file
6. Click "Publish release"

## Step 6: Commit and Deploy
```bash
# Add all files
git add .

# Commit changes
git commit -m "Ready for Heroku deployment"

# Push to main branch
git push origin main

# Deploy to Heroku
git push heroku main
```

## Step 7: Open Your App
```bash
heroku open
```

## Troubleshooting

### If deployment fails:
```bash
# Check logs
heroku logs --tail

# Restart app
heroku restart

# Check app status
heroku ps
```

### Common issues:
1. **Build timeout**: Model download taking too long
   - Solution: Use a faster hosting service or smaller model

2. **Memory limit**: App using too much RAM
   - Solution: Upgrade to paid plan or optimize model

3. **Port binding**: App not binding to correct port
   - Solution: Check Procfile configuration

### Current Status:
✅ All deployment files ready
✅ Dependencies installed
✅ Git repository initialized
⏳ Heroku CLI installation in progress
🔄 Model needs to be uploaded to GitHub releases
