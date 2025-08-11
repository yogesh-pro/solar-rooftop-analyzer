# Solar Rooftop Analyzer - Flask Version

**Professional Flask web application** for rooftop solar potential analysis.

## Features

- **Rooftop Detection**: Advanced computer vision model
- **Analysis**: OpenRouter API integration for intelligent recommendations
- **Cost Metrics**: Complete cost-benefit analysis with ROI calculations
- **Professional UI**: Modern Bootstrap interface with responsive design
- **Mobile Friendly**: Works seamlessly on all devices
- **Secure**: File upload validation and error handling
- **Fast**: Optimized for quick analysis and results

## Quick Start

### 1. Install Dependencies
```bash
cd Flask
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

### 3. Run the Application
```bash
python run_flask.py
```

### 4. Open Browser
Navigate to: http://localhost:5000

## 📁 Project Structure

```
Flask/
├── flask_app.py          # Main Flask application
├── run_flask.py          # Application runner script
├── model_loader.py       # AI model loading utilities
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template with Bootstrap
│   ├── index.html       # Upload page
│   └── results.html     # Results display
└── static/              # Static files
    ├── uploads/         # Temporary file uploads
    └── results/         # Generated visualizations
```

## 🔧 API Endpoints

### Web Interface
- `GET /` - Upload page
- `POST /analyze` - Process uploaded image

### REST API
- `POST /api/analyze` - JSON API for programmatic access

### Example API Usage
```bash
curl -X POST -F "file=@rooftop.jpg" http://localhost:5000/api/analyze
```

## Sample Output

For a 150m² rooftop:
- **Recommended Panels**: 25 panels
- **Total Capacity**: 6.25 kW
- **Yearly Production**: 9,000 kWh
- **Installation Cost**: ₹375,000
- **Yearly Savings**: ₹54,000
- **Payback Period**: 8.2 years

## ⚙️ Configuration

### Environment Variables
- `OPENROUTER_API_KEY` - Required for AI analysis
- `FLASK_ENV` - Set to `development` for debug mode
- `FLASK_PORT` - Custom port (default: 5000)

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: JPG, JPEG, PNG
- Minimum rooftop area: 10m²

## 🛠️ Development

### Local Development
```bash
export FLASK_ENV=development
export OPENROUTER_API_KEY="your_key"
python flask_app.py
```

### Production Deployment
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

## Security Features

- ✅ File type validation
- ✅ Secure filename handling
- ✅ File size limits
- ✅ Temporary file cleanup
- ✅ Error handling
- ✅ Input sanitization

## 🌐 Browser Support

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers

## 📝 License

This project is part of the Solar Rooftop Analyzer suite.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Ready to analyze rooftops with Flask!**
