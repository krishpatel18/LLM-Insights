#!/usr/bin/env python3
"""
Offline Transcript Q&A System
==============================

This script creates a local, offline Q&A system for sales call transcripts.
It loads transcript files, chunks them, embeds them using sentence-transformers,
and answers questions using a local LLM.

Requirements:
- sentence-transformers (for embeddings)
- local llm
- numpy (for similarity calculations)
- glob (built-in, for file loading)
"""

import os
import glob
import re
from typing import List, Tuple, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import json

class TranscriptQASystem:
    def __init__(self, transcript_dir: str = "transcripts", chunk_size: int = 500):
        """
        Initialize the Q&A system.
        
        Args:
            transcript_dir: Directory containing transcript files
            chunk_size: Maximum character size for each chunk
        """
        self.transcript_dir = transcript_dir
        self.chunk_size = chunk_size
        
        # Initialize models
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("Loading LLM model...")
        # Use Ollama for easier model management
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2:3b"  # llm model
        
        # Check if Ollama is running
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                print(f"   Ollama is running")
                print(f"   Available models:")
                models = response.json().get("models", [])
                for model in models:
                    print(f"    - {model['name']}")
                
                # Check if our model is available
                model_names = [m['name'] for m in models]
                if self.model_name in model_names:
                    print(f"   Model {self.model_name} is available")
                else:
                    print(f"    Model {self.model_name} not found")
                    print(f"   Run: ollama pull {self.model_name}")
            else:
                print(f"   Ollama not responding")
        except Exception as e:
            print(f"   Cannot connect to Ollama: {e}")
            print(f"   Please install and start Ollama first")
        
        # Storage for chunks and embeddings
        self.chunks = []
        self.chunk_embeddings = []
        
        # Load and process transcripts
        self._load_transcripts()
        self._create_chunks()
        self._embed_chunks()
        
    def _load_transcripts(self):
        """Load all transcript files from the transcripts directory."""
        print(f"Loading transcripts from {self.transcript_dir}/...")
        
        # Find all .txt files in the transcripts directory
        transcript_files = glob.glob(os.path.join(self.transcript_dir, "*.txt"))
        
        if not transcript_files:
            raise FileNotFoundError(f"No transcript files found in {self.transcript_dir}/")
        
        self.transcripts = []
        for file_path in transcript_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.transcripts.append(content)
                print(f"  Loaded: {os.path.basename(file_path)} ({len(content)} characters)")
        
        print(f"Total transcripts loaded: {len(self.transcripts)}")
    
    def _create_chunks(self):
        """Split transcripts into smaller chunks for better context management."""
        print("Creating text chunks...")
        
        for transcript in self.transcripts:
            # Split by timestamp lines (e.g., "0:02", "1:15")
            lines = transcript.split('\n')
            current_chunk = ""
            
            for line in lines:
                # Check if line is a timestamp (e.g., "0:02", "1:15")
                if re.match(r'^\d+:\d+$', line.strip()):
                    # If we have content in current_chunk and it's getting long, save it
                    if len(current_chunk) > self.chunk_size and current_chunk.strip():
                        self.chunks.append(current_chunk.strip())
                        current_chunk = ""
                    continue
                
                # Add line to current chunk
                current_chunk += line + " "
                
                # If chunk is getting long, save it and start new one
                if len(current_chunk) > self.chunk_size:
                    if current_chunk.strip():
                        self.chunks.append(current_chunk.strip())
                        current_chunk = ""
            
            # Add any remaining content as final chunk
            if current_chunk.strip():
                self.chunks.append(current_chunk.strip())
        
        print(f"Created {len(self.chunks)} chunks")
        
        # Show sample chunks for verification
        print("\nSample chunks:")
        for i, chunk in enumerate(self.chunks[:3]):
            print(f"  Chunk {i+1}: {chunk[:100]}...")
    
    def _embed_chunks(self):
        """Create embeddings for all text chunks."""
        print("Creating embeddings for chunks...")
        
        # Create embeddings for all chunks
        self.chunk_embeddings = self.embedding_model.encode(self.chunks)
        print(f"Embeddings created: {self.chunk_embeddings.shape}")
    
    def _find_relevant_chunks(self, question: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find the most relevant chunks for a given question.
        
        Args:
            question: The question to find relevant chunks for
            top_k: Number of top chunks to return
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        # Embed the question
        question_embedding = self.embedding_model.encode([question])
        
        # Calculate cosine similarity between question and all chunks
        similarities = []
        for chunk_embedding in self.chunk_embeddings:
            # Calculate cosine similarity
            similarity = np.dot(question_embedding[0], chunk_embedding) / (
                np.linalg.norm(question_embedding[0]) * np.linalg.norm(chunk_embedding)
            )
            similarities.append(similarity)
        
        # Get top-k most similar chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        relevant_chunks = []
        for idx in top_indices:
            relevant_chunks.append((self.chunks[idx], similarities[idx]))
        
        return relevant_chunks
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question based on the transcript content.
        
        Args:
            question: The question to answer
            
        Returns:
            A concise answer based on the transcript content
        """
        print(f"\nQuestion: {question}")
        print("Searching for relevant information...")
        
        # Find relevant chunks
        relevant_chunks = self._find_relevant_chunks(question, top_k=3)
        
        if not relevant_chunks:
            return "I couldn't find any relevant information in the transcripts to answer your question."
        
        # Prepare context for the LLM
        context = "\n\n".join([chunk for chunk, score in relevant_chunks])
        
        # Create prompt for the LLM
        prompt = f"""You are a helpful AI assistant analyzing sales call transcripts. Based on the provided transcript excerpts, answer the question concisely and accurately. Focus only on the information present in the transcripts. Do not include quotes or extra commentary.

Question: {question}

Relevant transcript excerpts:
{context}

Please provide a concise answer based only on the transcript information:"""
        
        print("Generating answer using Ollama...")
        
        try:
            # Generate answer using Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "max_tokens": 200
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "").strip()
                
                # Clean up the response
                answer = re.sub(r'^["\']|["\']$', '', answer)
                return answer
            else:
                return f"Error generating answer: {response.status_code}"
                
        except Exception as e:
            return f"Error generating answer: {e}"

def main():
    """Main function to run the Q&A system."""
    print("=" * 60)
    print("OFFLINE TRANSCRIPT Q&A SYSTEM")
    print("=" * 60)
    
    try:
        # Initialize the Q&A system
        qa_system = TranscriptQASystem()
        
        print("\n" + "=" * 60)
        print("SYSTEM READY - Ask your questions!")
        print("=" * 60)
        print("Type 'quit' or 'exit' to end the session")
        print()
        
        while True:
            # Get user question
            question = input("Enter your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not question:
                print("Please enter a question.")
                continue
            
            try:
                # Get answer
                answer = qa_system.answer_question(question)
                
                print("\nAnswer:")
                print("-" * 40)
                print(answer)
                print("-" * 40)
                
            except Exception as e:
                print(f"Error generating answer: {e}")
            
            print()
    
    except Exception as e:
        print(f"Error initializing system: {e}")
        print("Please check that all required models are installed and transcript files are available.")

if __name__ == "__main__":
    main()
