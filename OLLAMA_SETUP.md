# Ollama Setup for Llama 3.2 3B

##   **Installation Steps:**

### **1. Install Ollama**
```bash
# macOS (using Homebrew)
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from: https://ollama.ai/download
```

### **2. Start Ollama**
```bash
ollama serve
```

### **3. Download Llama 3.2 3B**
```bash
ollama pull llama3.2:3b
```

### **4. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

##   **Run the System**
```bash
python transcript_qa.py
```

## 💡 **Alternative Models to Try:**

If you want to experiment with other models:

```bash
# Smaller, faster models
ollama pull llama3.2:1b-instruct    # ~1.3GB
ollama pull phi3:mini               # ~1.5GB

# Larger, higher quality models  
ollama pull llama3.2:8b-instruct    # ~5GB
ollama pull llama3.2:70b-instruct   # ~40GB (best quality)
```

## 🔍 **Check Available Models**
```bash
ollama list
```

## ⚡ **Performance Notes:**
- **Llama 3.2 3B**: Good balance of speed/quality
- **First run**: ~30 seconds (model loading)
- **Subsequent runs**: ~5-10 seconds per question
- **Memory usage**: ~4-6GB during operation

##   **Troubleshooting:**

**"Ollama not responding"**
```bash
# Start Ollama service
ollama serve

# In another terminal, check status
ollama list
```

**"Model not found"**
```bash
# Download the model
ollama pull llama3.2:3b
```

##   **Benefits of This Setup:**
-  **Easier installation** than manual model downloads
-  **Better model quality** than GPT4All
-  **Automatic model management**
-  **Smaller disk space** requirements
-  **Faster inference** than larger models
-  **Easy model switching** between different sizes/qualities

##   **Advanced Usage:**

**Pull multiple models for comparison:**
```bash
ollama pull llama3.2:1b      # Fastest
ollama pull llama3.2:3b      # Balanced (recommended)
ollama pull llama3.2:8b      # Better quality
```

**Remove unused models:**
```bash
ollama rm llama3.2:1b        # Remove specific model
ollama rm --all               # Remove all models
```

**Update models:**
```bash
ollama pull llama3.2:3b      # Pulls latest version
```
