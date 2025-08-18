#!/usr/bin/env python3
"""
Test script for the Offline Transcript Q&A System
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print(" Testing imports...")
    
    try:
        import numpy
        print(" numpy imported successfully")
    except ImportError:
        print(" numpy import failed")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print(" sentence-transformers imported successfully")
    except ImportError:
        print(" sentence-transformers import failed")
        return False
    
    try:
        import requests
        print(" requests imported successfully")
    except ImportError:
        print(" requests import failed")
        return False
    
    return True

def test_transcript_loading():
    """Test if transcript files can be loaded."""
    print("\n📁 Testing transcript loading...")
    
    transcript_dir = "transcripts"
    if not os.path.exists(transcript_dir):
        print(f" Transcript directory '{transcript_dir}' not found")
        return False
    
    transcript_files = [f for f in os.listdir(transcript_dir) if f.endswith('.txt')]
    if not transcript_files:
        print(f" No .txt files found in '{transcript_dir}' directory")
        return False
    
    print(f" Found {len(transcript_files)} transcript files:")
    for file in transcript_files:
        file_path = os.path.join(transcript_dir, file)
        size = os.path.getsize(file_path)
        print(f"   - {file} ({size} bytes)")
    
    return True

def test_qa_system():
    """Test if the Q&A system can be initialized."""
    print("\n Testing Q&A system initialization...")
    
    try:
        from transcript_qa import TranscriptQASystem
        print(" TranscriptQASystem class imported successfully")
        
        # Try to create an instance (this will test model loading)
        print("   Initializing system (this may take a few minutes on first run)...")
        qa_system = TranscriptQASystem()
        print(" Q&A system initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f" Failed to initialize Q&A system: {e}")
        return False

def run_sample_questions():
    """Run a few sample questions to test the system."""
    print("\n Testing sample questions...")
    
    try:
        from transcript_qa import TranscriptQASystem
        
        # Initialize system
        qa_system = TranscriptQASystem()
        
        # Sample questions
        sample_questions = [
            "What are the pricing options for lawn mowing?",
            "What is the cancellation policy?",
            "Do they offer bagging services?"
        ]
        
        for question in sample_questions:
            print(f"\nQuestion: {question}")
            print("-" * 50)
            
            try:
                answer = qa_system.answer_question(question)
                print(f"Answer: {answer}")
                print(" Question answered successfully")
            except Exception as e:
                print(f" Failed to answer question: {e}")
        
        return True
        
    except Exception as e:
        print(f" Failed to run sample questions: {e}")
        return False

def main():
    """Main test function."""
    print(" Offline Transcript Q&A System - Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4  # 4 tests: imports, transcript loading, Q&A init, sample questions
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: Transcript loading
    if test_transcript_loading():
        tests_passed += 1
    
    # Test 3: Q&A system initialization
    if test_qa_system():
        tests_passed += 1
    
    # Test 4: Sample questions (optional - comment out if you want to skip)
    if run_sample_questions():
        tests_passed += 1
    
    # Results
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The system is ready to use.")
        print("Run: python transcript_qa.py")
    else:
        print(" Some tests failed. Please check the errors above.")
        print(" Try running: python setup.py")

if __name__ == "__main__":
    main()
