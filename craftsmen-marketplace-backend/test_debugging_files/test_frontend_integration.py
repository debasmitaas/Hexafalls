#!/usr/bin/env python3
"""
Test the complete frontend-to-backend integration by simulating the exact call
that the Flutter frontend makes
"""

import requests
import os
from pathlib import Path

# Backend URL (matching frontend configuration)
BACKEND_URL = "http://localhost:8000"

def test_native_products_endpoint():
    """Test the /native_products/create-and-post-native endpoint"""
    print("🧪 Testing Frontend Integration (Native Products Endpoint)...")
    
    # Check if we have any test images in uploads folder
    uploads_dir = Path("craftsmen-marketplace-backend/uploads")
    test_images = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.png")) + list(uploads_dir.glob("*.JPG"))
    
    if not test_images:
        print("❌ No test images found in uploads directory")
        print(f"   Checked: {uploads_dir.absolute()}")
        return False
    
    # Use the first available image
    test_image_path = test_images[0]
    print(f"📷 Using test image: {test_image_path.name}")
    
    try:
        with open(test_image_path, 'rb') as img_file:
            # Prepare the multipart form data (exactly like Flutter sends)
            files = {
                'image_file': (test_image_path.name, img_file, 'image/jpeg')
            }
            
            data = {
                'name': 'Test Handmade Pottery Bowl',
                'price': '450',
                'description': 'Beautiful handcrafted pottery bowl with traditional design',
                'category': 'pottery',
                'owner_id': '1',
                'platforms': '["facebook", "instagram"]'
            }
            
            print("📡 Sending request to backend...")
            response = requests.post(
                f"{BACKEND_URL}/native_products/create-and-post-native",
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Frontend Integration - SUCCESS")
                print(f"   Product ID: {result.get('product', {}).get('id')}")
                print(f"   AI Caption: {result.get('product', {}).get('ai_caption', 'No caption')[:100]}...")
                print(f"   Facebook Post ID: {result.get('product', {}).get('facebook_post_id', 'None')}")
                print(f"   Instagram Post ID: {result.get('product', {}).get('instagram_post_id', 'None')}")
                return True
            else:
                print(f"❌ Frontend Integration - FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Frontend Integration - ERROR: {e}")
        return False

def main():
    """Test the complete integration"""
    print("🚀 Testing Complete Frontend-Backend Integration\n")
    
    success = test_native_products_endpoint()
    
    print("\n📊 INTEGRATION TEST SUMMARY:")
    if success:
        print("🎉 SUCCESS! The frontend integration is working correctly.")
        print("   Your Flutter app should be able to:")
        print("   ✅ Upload images")
        print("   ✅ Create products") 
        print("   ✅ Generate AI captions")
        print("   ✅ Get responses back")
    else:
        print("⚠️  Integration test failed. Check the backend logs for more details.")

if __name__ == "__main__":
    main()
