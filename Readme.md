# Solar Rooftop Analyzer

Professional Flask web application for rooftop solar potential analysis with AI.

## Features
- Rooftop detection (Computer Vision)
- AI recommendations via OpenRouter
- Cost-benefit metrics with ROI
- Modern, responsive UI (Bootstrap)
- Secure uploads and error handling

## Quick Start (uv)

1) Setup
```bash
./setup.sh
```

2) Configure API key
Create or edit `Flask/.env`:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

3) Run
```bash
./run-flask.sh
```
App: http://localhost:8080

## Alternative: Manual
```bash
uv venv
source .venv/bin/activate
uv pip install -r Flask/requirements.txt
cd Flask
python server.py
```

## Project Structure
```
Flask/
├── main.py            # Core Flask app (routes, analysis)
├── server.py          # App runner (host/port)
├── model_loader.py    # Model loading utils
├── templates/         # HTML templates (base, index, results)
├── static/            # Static assets (uploads, results)
└── .env               # Environment (OPENROUTER_API_KEY)
pyproject.toml         # uv project config
uv.lock                # lockfile
run-flask.sh           # helper to run app
setup.sh               # helper to set up env
```

## API
- Web: `GET /` upload/entry, `POST /analyze`, `POST /analyze-manual`
- REST: `POST /api/analyze` (multipart/form-data or JSON)
```bash
curl -X POST -F "file=@your_image.jpg" http://localhost:8080/api/analyze
```

## Requirements
- Python 3.10+
- OpenRouter API key (https://openrouter.ai/)

## Notes
- Environment is loaded from `Flask/.env`.
- Model file may be downloaded automatically if missing.