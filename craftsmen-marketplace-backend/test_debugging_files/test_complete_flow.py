#!/usr/bin/env python3
"""
Complete Flow Test: Frontend Image + Gemini Caption → Instagram Post
Tests the entire flow from image upload to Instagram posting
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://192.168.133.28:8000"  # Use your backend URL
TEST_IMAGE_PATH = "uploads/test_image.jpg"  # Path to test image

def test_complete_flow():
    """Test the complete flow: Image → Gemini Caption → Instagram Post"""
    
    print("🚀 Testing Complete Flow: Image → Gemini Caption → Instagram Post")
    print("=" * 60)
    
    # Step 1: Test AI Caption Generation
    print("\n📝 Step 1: Testing AI Caption Generation...")
    caption_data = {
        "product_name": "Beautiful Handmade Pottery Vase",
        "price": 1500.0,
        "description": "Elegant ceramic vase with traditional Bengali patterns",
        "category": "pottery"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/ai/generate-caption",
            json=caption_data,
            timeout=30
        )
        print(f"Caption Response Status: {response.status_code}")
        print(f"Caption Response: {response.text}")
        
        if response.status_code == 200:
            caption_result = response.json()
            generated_caption = caption_result.get('caption', '')
            print(f"✅ Generated Caption: {generated_caption}")
        else:
            print(f"❌ Caption generation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Caption generation error: {e}")
        return False
    
    # Step 2: Test Complete Upload and Post
    print(f"\n📸 Step 2: Testing Complete Upload and Post Flow...")
    
    # Check if test image exists
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        print("Please place a test image in the uploads folder")
        return False
    
    try:
        # Prepare multipart form data
        with open(TEST_IMAGE_PATH, 'rb') as image_file:
            files = {'file': ('test_image.jpg', image_file, 'image/jpeg')}
            data = {
                'product_name': 'Beautiful Handmade Pottery Vase',
                'price': '1500',
                'caption': generated_caption,  # Use the generated caption
                'description': 'Elegant ceramic vase with traditional Bengali patterns',
                'category': 'pottery'
            }
            
            print(f"Posting with caption: {generated_caption[:50]}...")
            
            response = requests.post(
                f"{BACKEND_URL}/native_products/create-and-post-native",
                files=files,
                data=data,
                timeout=60
            )
            
        print(f"Post Response Status: {response.status_code}")
        print(f"Post Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Complete flow successful!")
            print(f"Product ID: {result.get('product', {}).get('id')}")
            print(f"Instagram Post ID: {result.get('product', {}).get('instagram_post_id')}")
            print(f"Facebook Post ID: {result.get('product', {}).get('facebook_post_id')}")
            return True
        else:
            print(f"❌ Post failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Post error: {e}")
        return False

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend is running: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Complete Frontend-Backend Flow")
    print("=" * 50)
    
    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start the backend server first.")
        exit(1)
    
    # Test complete flow
    success = test_complete_flow()
    
    if success:
        print("\n🎉 All tests passed! Your complete flow is working.")
        print("\n📱 Frontend Integration Guide:")
        print("1. User selects image in Flutter app")
        print("2. User enters product name and price")
        print("3. App calls /ai/generate-caption to get Gemini caption")
        print("4. User can preview and edit the caption")
        print("5. App calls /native_products/create-and-post-native with image + caption")
        print("6. Backend posts to Instagram with the generated caption")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
