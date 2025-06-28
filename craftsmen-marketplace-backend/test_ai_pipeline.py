#!/usr/bin/env python3
"""
Test script to verify the AI caption generation pipeline works end-to-end
"""

import requests
import json
from pathlib import Path

# Backend URL
BACKEND_URL = "http://localhost:8000"

def test_ai_caption_generation():
    """Test the AI caption generation endpoint directly"""
    print("🧪 Testing AI Caption Generation...")
    
    # Test payload
    payload = {
        "product_name": "Handmade Ceramic Vase",
        "price": "750",
        "description": "Beautiful blue ceramic vase with traditional patterns",
        "category": "pottery"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/ai/generate-caption",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI Caption Generation - SUCCESS")
            print(f"   Caption: {result.get('caption', 'No caption')}")
            print(f"   Hashtags: {result.get('hashtags', [])}")
            return True
        else:
            print(f"❌ AI Caption Generation - FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ AI Caption Generation - ERROR: {e}")
        return False

def test_ai_service_status():
    """Test if AI service is properly configured"""
    print("🔍 Testing AI Service Status...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/ai/test")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('model_configured'):
                print("✅ AI Service Status - CONFIGURED")
                return True
            else:
                print("❌ AI Service Status - NOT CONFIGURED")
                return False
        else:
            print(f"❌ AI Service Status - FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ AI Service Status - ERROR: {e}")
        return False

def test_backend_connectivity():
    """Test if backend is running and accessible"""
    print("🌐 Testing Backend Connectivity...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/")
        
        if response.status_code == 200:
            print("✅ Backend Connectivity - SUCCESS")
            return True
        else:
            print(f"❌ Backend Connectivity - FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Backend Connectivity - ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Caption Generation Pipeline Tests\n")
    
    # Test 1: Backend connectivity
    backend_ok = test_backend_connectivity()
    print()
    
    # Test 2: AI service status
    ai_status_ok = test_ai_service_status()
    print()
    
    # Test 3: AI caption generation
    ai_caption_ok = test_ai_caption_generation()
    print()
    
    # Summary
    print("📊 TEST SUMMARY:")
    print(f"   Backend Connectivity: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   AI Service Status: {'✅ PASS' if ai_status_ok else '❌ FAIL'}")
    print(f"   AI Caption Generation: {'✅ PASS' if ai_caption_ok else '❌ FAIL'}")
    
    if all([backend_ok, ai_status_ok, ai_caption_ok]):
        print("\n🎉 ALL TESTS PASSED! The AI caption generation pipeline is working correctly.")
        print("   Your frontend should be able to get AI-generated captions successfully.")
    else:
        print("\n⚠️  Some tests failed. Please check the backend configuration.")

if __name__ == "__main__":
    main()
