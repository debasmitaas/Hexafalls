#!/usr/bin/env python3
"""
Test Gemini API and Instagram credentials from .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_variables():
    """Check if all required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    
    # Gemini API
    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"   Gemini API Key: {'✅ SET' if gemini_key else '❌ NOT SET'}")
    if gemini_key:
        print(f"   Key starts with: {gemini_key[:10]}...")
    
    # Instagram credentials
    ig_username = os.getenv('INSTAGRAM_USERNAME')
    ig_password = os.getenv('INSTAGRAM_PASSWORD')
    print(f"   Instagram Username: {'✅ SET' if ig_username else '❌ NOT SET'}")
    print(f"   Instagram Password: {'✅ SET' if ig_password else '❌ NOT SET'}")
    
    if ig_username:
        print(f"   Username: {ig_username}")
    if ig_password:
        print(f"   Password: {'*' * len(ig_password)}")
    
    return bool(gemini_key and ig_username and ig_password)

def test_gemini_direct():
    """Test Gemini API directly"""
    print("\n🤖 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        
        # Configure Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No Gemini API key found")
            return False
        
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Write a short Instagram caption for a handmade wooden bowl priced at 500 rupees")
        
        print("✅ Gemini API - SUCCESS")
        print(f"   Generated caption: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API - ERROR: {e}")
        return False

def test_instagram_package():
    """Test if Instagram package can be imported"""
    print("\n📱 Testing Instagram Package...")
    
    try:
        from InstagramAPI import InstagramAPI
        print("✅ InstagramAPI package - IMPORTED")
        
        # Try to create instance (don't login yet)
        username = os.getenv('INSTAGRAM_USERNAME')
        password = os.getenv('INSTAGRAM_PASSWORD')
        
        if username and password:
            api = InstagramAPI(username, password)
            print("✅ InstagramAPI instance - CREATED")
            return True
        else:
            print("❌ Instagram credentials not found")
            return False
            
    except ImportError as e:
        print(f"❌ InstagramAPI package - IMPORT ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ InstagramAPI instance - ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Environment and API Tests\n")
    
    # Test 1: Environment variables
    env_ok = check_env_variables()
    
    # Test 2: Gemini API
    gemini_ok = test_gemini_direct()
    
    # Test 3: Instagram package
    instagram_ok = test_instagram_package()
    
    # Summary
    print("\n📊 TEST SUMMARY:")
    print(f"   Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"   Gemini API: {'✅ PASS' if gemini_ok else '❌ FAIL'}")
    print(f"   Instagram Package: {'✅ PASS' if instagram_ok else '❌ FAIL'}")
    
    if all([env_ok, gemini_ok, instagram_ok]):
        print("\n🎉 ALL TESTS PASSED! Ready to implement combined service.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
