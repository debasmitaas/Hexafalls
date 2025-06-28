"""
Test script to verify Google Cloud Speech-to-Text configuration
"""
import os
from app.core.config import settings

def test_google_cloud_setup():
    print("🧪 Testing Google Cloud Configuration...")
    print(f"📋 Project ID: {settings.google_cloud_project}")
    print(f"🔑 Credentials Path: {settings.google_application_credentials}")
    
    # Check if credentials file exists
    if settings.google_application_credentials:
        creds_path = settings.google_application_credentials
        if os.path.exists(creds_path):
            print(f"✅ Credentials file found: {creds_path}")
        else:
            print(f"❌ Credentials file NOT found: {creds_path}")
            print("📝 Please make sure to:")
            print("   1. Download your service account JSON key")
            print("   2. Place it at: credentials/service-account-key.json")
            return False
    
    # Test Google Cloud Speech client
    try:
        from google.cloud import speech
        client = speech.SpeechClient()
        print("✅ Google Cloud Speech client initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing Speech client: {str(e)}")
        return False

def test_gemini_api():
    print("\n🤖 Testing Gemini AI Configuration...")
    if settings.gemini_api_key and settings.gemini_api_key != "your-gemini-api-key":
        print("✅ Gemini API key configured")
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini AI initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Error with Gemini AI: {str(e)}")
            print("🔍 Check if your API key is valid")
            return False
    else:
        print("❌ Gemini API key not configured or using placeholder")
        return False

if __name__ == "__main__":
    print("🚀 Google Cloud & AI Services Configuration Test")
    print("=" * 50)
    
    google_ok = test_google_cloud_setup()
    gemini_ok = test_gemini_api()
    
    print("\n📊 Test Results:")
    print(f"Google Cloud Speech: {'✅ Ready' if google_ok else '❌ Needs Setup'}")
    print(f"Gemini AI: {'✅ Ready' if gemini_ok else '❌ Needs Setup'}")
    
    if google_ok and gemini_ok:
        print("\n🎉 All AI services are configured and ready!")
    else:
        print("\n⚠️  Some services need configuration. Check the messages above.")
