import os
import requests
import torch
import streamlit as st
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
                    # Show progress
                    progress = (downloaded / total_size) * 100
                    print(f"Download progress: {progress:.1f}%")
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
    """Load model with multiple fallback options"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Define model sources in order of preference
    model_sources = [
        # Local file (for development)
        "./rooftop_best_model.pt",
        "https://github.com/yogesh-pro/solar-rooftop-analyzer/releases/download/Model/rooftop_best_model.pt",
        # Add your model URL here (Google Drive, Dropbox, etc.)
        # "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID",
        # "https://your-cloud-storage.com/rooftop_best_model.pt"
    ]
    
    for source in model_sources:
        try:
            if source.startswith("http"):
                # Download from URL
                local_path = "./models/rooftop_best_model.pt"
                downloaded_path = download_model_from_url(source, local_path)
                if downloaded_path:
                    model = torch.load(downloaded_path, map_location=device, weights_only=False)
                    model.eval()
                    model.to(device)
                    return model, device
            else:
                # Load local file
                if os.path.exists(source):
                    model = torch.load(source, map_location=device, weights_only=False)
                    model.eval()
                    model.to(device)
                    return model, device
        except Exception as e:
            print(f"Failed to load model from {source}: {e}")
            continue
    
    # If no model found, show error
    st.error("""
    🚨 **Model file not found!**
    
    To fix this issue:
    1. Upload your model file to a cloud storage service (Google Drive, Dropbox, etc.)
    2. Get a direct download link
    3. Update the `model_sources` list in `model_loader.py`
    
    Or contact the developer for the model file.
    """)
    st.stop()
    return None, None
