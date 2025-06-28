#!/usr/bin/env python3
"""
Test script to verify the Craftsmen Marketplace Backend setup
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def test_health_check():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8000")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   App: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")
        return False

def test_products_endpoint():
    """Test the products endpoint"""
    try:
        response = requests.get(f"{API_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Products endpoint working (found {len(products)} products)")
            return True
        else:
            print(f"❌ Products endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Products endpoint error: {str(e)}")
        return False

def test_orders_endpoint():
    """Test the orders endpoint"""
    try:
        response = requests.get(f"{API_URL}/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Orders endpoint working (found {len(orders)} orders)")
            return True
        else:
            print(f"❌ Orders endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Orders endpoint error: {str(e)}")
        return False

def test_create_sample_product():
    """Test creating a sample product"""
    try:
        # Create a simple test image
        from PIL import Image
        import io
        
        # Create a simple colored image
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Upload the image
        files = {'file': ('test_image.png', img_byte_arr, 'image/png')}
        response = requests.post(f"{API_URL}/products/upload-image", files=files)
        
        if response.status_code == 200:
            upload_data = response.json()
            print(f"✅ Image upload working")
            print(f"   Uploaded: {upload_data.get('filename')}")
            return True
        else:
            print(f"❌ Image upload failed: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Image upload error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Craftsmen Marketplace Backend Tests")
    print("=" * 50)
    
    tests = [
        ("Server Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Products Endpoint", test_products_endpoint),
        ("Orders Endpoint", test_orders_endpoint),
        ("Image Upload", test_create_sample_product),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        if test_func():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is working correctly.")
        print("\n📝 Next Steps:")
        print("1. Configure your API keys in the .env file")
        print("2. Test speech-to-text functionality")
        print("3. Set up social media integrations")
        print("4. Connect your Flutter frontend")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the server is running: uv run python main.py")
        print("2. Check if all dependencies are installed: uv sync")
        print("3. Verify your Python environment is active")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
