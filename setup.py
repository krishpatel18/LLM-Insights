#!/usr/bin/env python3
"""
Setup script for the Offline Transcript Q&A System
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print(" Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f" Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\n Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(" Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Failed to install dependencies: {e}")
        return False

def check_ollama():
    """Check if Ollama is installed and running."""
    print("\n Checking for Ollama...")
    
    try:
        # Check if ollama command exists
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f" Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            print(" Ollama command failed")
            return False
    except FileNotFoundError:
        print(" Ollama not found in PATH")
        return False

def check_ollama_service():
    """Check if Ollama service is running."""
    print("\n Checking if Ollama service is running...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print(" Ollama service is running")
            return True
        else:
            print(" Ollama service not responding")
            return False
    except Exception as e:
        print(f" Cannot connect to Ollama service: {e}")
        return False

def check_models():
    """Check if required models are available."""
    print("\n Checking for required models...")
    
    # Check embedding model (will be downloaded automatically)
    print(" Embedding model will be downloaded automatically on first run")
    
    # Check Ollama models
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f" Found {len(models)} Ollama models:")
                for model in models:
                    print(f"   - {model['name']} ({model['size']})")
                
                # Check if our target model is available
                target_model = "llama3.2:3b"
                model_names = [m['name'] for m in models]
                if target_model in model_names:
                    print(f" Target model '{target_model}' is available")
                    return True
                else:
                    print(f" Target model '{target_model}' not found")
                    return False
            else:
                print(" No Ollama models found")
                return False
        else:
            print(" Ollama service not responding")
            return False
    except Exception as e:
        print(f" Error checking models: {e}")
        return False

def install_ollama_instructions():
    """Provide instructions for installing Ollama."""
    print("\n OLLAMA INSTALLATION INSTRUCTIONS")
    print("=" * 50)
    print("You need to install Ollama to run this system:")
    print()
    print("1. Install Ollama:")
    print("   macOS: brew install ollama")
    print("   Linux: curl -fsSL https://ollama.ai/install.sh | sh")
    print("   Windows: Download from https://ollama.ai/download")
    print()
    print("2. Start Ollama service:")
    print("   ollama serve")
    print()
    print("3. Download the required model:")
    print("   ollama pull llama3.2:3b")
    print()
    print("4. Run the script again: python setup.py")

def download_model_instructions():
    """Provide instructions for downloading models."""
    print("\n MODEL DOWNLOAD INSTRUCTIONS")
    print("=" * 50)
    print("You need to download the required model:")
    print()
    print("1. Make sure Ollama is running:")
    print("   ollama serve")
    print()
    print("2. Download the model:")
    print("   ollama pull llama3.2:3b")
    print()
    print("3. Run the script again: python setup.py")

def main():
    """Main setup function."""
    print(" Offline Transcript Q&A System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n Try installing manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check Ollama installation
    ollama_installed = check_ollama()
    
    if not ollama_installed:
        install_ollama_instructions()
        sys.exit(1)
    
    # Check Ollama service
    if not check_ollama_service():
        print("\n Start Ollama service:")
        print("ollama serve")
        sys.exit(1)
    
    # Check models
    models_available = check_models()
    
    if not models_available:
        download_model_instructions()
    else:
        print("\n Setup complete! You can now run:")
        print("python transcript_qa.py")

if __name__ == "__main__":
    main()
