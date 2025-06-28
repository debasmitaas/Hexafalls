import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Test Gemini directly
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {api_key is not None}")
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content("Say hello!")
        print(f"Gemini Response: {response.text}")
        print("✅ Gemini is working!")
        
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
else:
    print("❌ No API key found")
