#!/usr/bin/env python3
"""
Download Phi-3-mini 128k GGUF model optimized for CPU inference
"""

import os
import requests
from huggingface_hub import hf_hub_download
import sys

def download_with_progress(url, filename):
    """Download file with progress bar"""
    print(f"Downloading {filename}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                if total_size > 0:
                    percent = (downloaded_size / total_size) * 100
                    print(f"\rProgress: {percent:.1f}% ({downloaded_size}/{total_size} bytes)", end='')
    
    print(f"\n✅ Downloaded {filename}")

def main():
    models_dir = "/app/models"
    os.makedirs(models_dir, exist_ok=True)
    
    # Phi-3-mini 128k Q4_K_M model - official Microsoft model
    model_info = {
        "repo_id": "eccheng/Phi-3-mini-128k-instruct-Q4_0-GGUF",
        "filename": "eccheng/Phi-3-mini-128k-instruct-Q4_0-GGUF",
        "local_filename": "phi-3-mini-128k-q4.gguf"
    }
    
    model_path = os.path.join(models_dir, model_info["local_filename"])
    
    # Check if model already exists
    if os.path.exists(model_path):
        print(f"✅ Model already exists: {model_path}")
        return
    
    print(f"🔄 Downloading Phi-3-mini 128k model...")
    print(f"   Repository: {model_info['repo_id']}")
    print(f"   Filename: {model_info['filename']}")
    print(f"   Quantization: Q4_K_M (optimal for CPU)")
    print(f"   Context: 128k tokens")
    print(f"   Target RAM usage: ~4-5GB")
    
    try:
        # Download using huggingface_hub
        downloaded_path = hf_hub_download(
            repo_id=model_info["repo_id"],
            filename=model_info["filename"],
            local_dir=models_dir,
            local_dir_use_symlinks=False
        )
        
        # Rename to our preferred name
        if downloaded_path != model_path:
            os.rename(downloaded_path, model_path)
        
        print(f"✅ Model downloaded successfully to: {model_path}")
        
        # Print model info
        size = os.path.getsize(model_path) / (1024**3)  # GB
        print(f"📊 Model size: {size:.2f} GB")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
