import os
import requests
import torch
from pathlib import Path

def download_model_from_url(url, local_path):
    """Download model from URL if not exists locally"""
    local_path = Path(local_path)
    
    if local_path.exists():
        print(f"Model already exists at {local_path}")
        return str(local_path)
    
    print(f"Downloading model from {url}...")
    
    try:
        # Create directory if it doesn't exist
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(local_path, 'wb') as f:
            if total_size > 0:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Show progress in console every 10MB
                    if downloaded % (1024 * 1024 * 10) == 0:
                        progress = downloaded / total_size * 100
                        print(f"Downloaded {downloaded // 1024 // 1024} MB / {total_size // 1024 // 1024} MB ({progress:.1f}%)")
            else:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Model downloaded successfully to {local_path}")
        return str(local_path)
    except Exception as e:
        print(f"Error downloading model: {e}")
        if local_path.exists():
            local_path.unlink()  # Remove partial download
        return None

def load_model_with_fallback():
    """
    Load model with multiple fallback sources
    Returns: (model, device) tuple
    """
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    print("Loading AI model...")
    
    # Define model sources in order of preference
    model_sources = [
        # Local file (for development)
        "./rooftop_best_model.pt",
        "https://github.com/yogesh-pro/solar-rooftop-analyzer/releases/download/Model/rooftop_best_model.pt",
        # Add your model URL here (Google Drive, Dropbox, etc.)
        # "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID",
        # "https://your-cloud-storage.com/rooftop_best_model.pt"
    ]
    
    for i, source in enumerate(model_sources):
        try:
            print(f"🔄 Trying source {i+1}/{len(model_sources)}: {source[:50]}...")
            
            if source.startswith("http"):
                # Download from URL
                local_path = "./models/rooftop_best_model.pt"
                downloaded_path = download_model_from_url(source, local_path)
                if downloaded_path:
                    model = torch.load(downloaded_path, map_location=device, weights_only=False)
                    model.eval()
                    model.to(device)
                    print("✅ Model loaded successfully!")
                    return model, device
            else:
                # Load local file
                if os.path.exists(source):
                    model = torch.load(source, map_location=device, weights_only=False)
                    model.eval()
                    model.to(device)
                    print("✅ Model loaded successfully!")
                    return model, device
                else:
                    print(f"❌ Local file not found: {source}")
        except Exception as e:
            print(f"❌ Failed to load from {source}: {str(e)[:100]}...")
            continue

    # If no model found, show detailed error
    error_msg = """
🚨 Model file not found!

For the app to work, the model file needs to be available.

📋 To fix this:
1. Go to: https://github.com/yogesh-pro/solar-rooftop-analyzer/releases
2. Click: "Create a new release"
3. Tag version: Model
4. Upload: Your rooftop_best_model.pt file (86MB)
5. Publish: The release
6. Restart: This Flask app

🔧 Alternative Solutions:
- Copy model file to Flask directory
- Upload to Google Drive and update the URL in model_loader.py
- Use Hugging Face Hub for model hosting

Note: This is a one-time setup. Once uploaded, the model will be automatically downloaded.
    """
    
    print(error_msg)
    raise FileNotFoundError("Model file not found. Please check the model_loader.py configuration.")
