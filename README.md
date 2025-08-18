# Offline Transcript Q&A System

A local, offline question-answering system for sales call transcripts that uses sentence embeddings and a local LLM to provide answers without any internet connection.

## Features

- **Fully Offline**: No API calls or internet connection required
- **Smart Chunking**: Automatically splits transcripts into optimal chunks (~500 characters)
- **Semantic Search**: Uses sentence-transformers for intelligent content retrieval
- **Local LLM**: Ollama with Llama 3.2 3B for generating answers locally
- **One-shot Processing**: Fresh data processing each time you run the script

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first run will download the embedding model (~90MB) automatically.

### 2. Install and Setup Ollama

#### Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from: https://ollama.ai/download
```

#### Start Ollama Service
```bash
ollama serve
```

#### Download Required Model
```bash
ollama pull llama3.2:3b
```

**Model Size**: ~2GB

### 3. Run the System

```bash
python transcript_qa.py
```

## Sample Questions to Try

- "What are the pricing options for lawn mowing services?"
- "What is the cancellation policy?"
- "Do they offer bagging services?"
- "What areas do they service?"
- "What is the long grass policy?"
- "How far in advance do you need to book?"

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for smooth operation)
- **Storage**: ~3GB free space for models
- **OS**: Windows, macOS, or Linux

## How It Works

1. **Loading**: Reads all `.txt` files from the `transcripts/` directory
2. **Chunking**: Splits transcripts into ~500 character chunks at natural break points (timestamps)
3. **Embedding**: Creates vector representations of each chunk using sentence-transformers
4. **Question Processing**: When you ask a question, it gets embedded and compared to all chunks
5. **Retrieval**: Finds the 3 most relevant chunks using cosine similarity
6. **Answer Generation**: Passes relevant chunks to the local Llama 3.2 3B model via Ollama to generate a concise answer

## Troubleshooting

### Common Issues

**"No module named 'sentence_transformers'"**
```bash
pip install sentence-transformers
```

**"Ollama not found"**
```bash
# Install Ollama
brew install ollama  # macOS
# or download from https://ollama.ai/download
```

**"Ollama service not responding"**
```bash
# Start Ollama service
ollama serve
```

**"Model not found" error**
```bash
# Download the required model
ollama pull llama3.2:3b
```

**Slow performance**
- The first run is slower due to model loading
- Subsequent runs will be faster
- Consider using a smaller model for faster inference: `ollama pull llama3.2:1b`

### Model Management

**List available models:**
```bash
ollama list
```

**Download additional models:**
```bash
# Smaller, faster models
ollama pull llama3.2:1b        # ~1.3GB
ollama pull phi3:mini          # ~1.5GB

# Larger, higher quality models
ollama pull llama3.2:8b        # ~5GB
ollama pull llama3.2:70b       # ~40GB (best quality)
```

## Customization

### Change Chunk Size
Modify the `chunk_size` parameter in the `TranscriptQASystem` constructor:

```python
qa_system = TranscriptQASystem(chunk_size=300)  # Smaller chunks
```

### Use Different Models
Change the model name in the constructor:

```python
# Different Ollama models
self.model_name = "llama3.2:1b"      # Faster, smaller
self.model_name = "llama3.2:8b"      # Better quality
self.model_name = "phi4:14b"         # Alternative model
```

### Adjust Similarity Search
Modify the `top_k` parameter in `_find_relevant_chunks()`:

```python
relevant_chunks = self._find_relevant_chunks(question, top_k=5)  # More context
```

## Performance Notes

- **First Run**: ~2-3 minutes (model loading + processing)
- **Subsequent Runs**: ~30 seconds (model loading + processing)
- **Question Answering**: ~5-15 seconds per question
- **Memory Usage**: ~4-6GB during operation
- **Model Size**: ~2GB