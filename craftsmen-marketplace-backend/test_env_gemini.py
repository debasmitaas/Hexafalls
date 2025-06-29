#!/usr/bin/env python3
"""
Quick test to check if Gemini API is working
"""

import os
import sys
import google.generativeai as genai
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_gemini():
    """Test Gemini API connection and generation"""
    print("🧪 Testing Gemini AI API...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Try different model names
        model_names = ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
        for model_name in model_names:
            try:
                print(f"🔄 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Test caption generation
                prompt = """Generate an engaging Instagram caption for a handmade wooden bowl priced at 500 rupees. 
                Make it creative and include relevant hashtags."""
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    print(f"✅ Gemini AI ({model_name}) - SUCCESS!")
                    print(f"   Generated Caption: {response.text[:100]}...")
                    return True
                    
            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue
        
        print("❌ All Gemini models failed")
        return False
        
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🔍 Checking Environment Variables...")
    
    required_vars = [
        'GEMINI_API_KEY',
        'INSTAGRAM_USERNAME', 
        'INSTAGRAM_PASSWORD'
    ]
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var or 'KEY' in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not found")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("🚀 Environment and Gemini API Test\n")
    
    # Test environment
    env_ok = test_environment()
    
    # Test Gemini
    gemini_ok = test_gemini()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"   Environment: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"   Gemini API: {'✅ PASS' if gemini_ok else '❌ FAIL'}")
    
    if env_ok and gemini_ok:
        print("\n🎉 ALL TESTS PASSED! Ready to generate captions and post to Instagram!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
