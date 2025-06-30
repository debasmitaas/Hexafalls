#!/usr/bin/env python3
"""
Test Instagram posting functionality with your credentials
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.instagram_service import instagram_service
from app.core.config import settings
import asyncio
from pathlib import Path

async def test_instagram_connection():
    """Test Instagram connection"""
    print("🔍 Testing Instagram Connection...")
    print(f"   Username: {settings.instagram_username}")
    print(f"   Password: {'*' * len(settings.instagram_password) if settings.instagram_password else 'Not set'}")
    
    result = instagram_service.test_connection()
    
    if result["connected"]:
        print("✅ Instagram Connection - SUCCESS")
        print(f"   Connected as: {result['username']}")
        return True
    else:
        print("❌ Instagram Connection - FAILED")
        print(f"   Error: {result['error']}")
        return False

async def test_instagram_post():
    """Test posting to Instagram"""
    print("\n📸 Testing Instagram Photo Upload...")
    
    # Find a test image in uploads directory
    uploads_dir = Path("uploads")
    test_images = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.png")) + list(uploads_dir.glob("*.JPG"))
    
    if not test_images:
        print("❌ No test images found in uploads directory")
        return False
    
    test_image = test_images[0]
    print(f"   Using image: {test_image.name}")
    
    # Test caption
    caption = "Test post from Craftsmen Marketplace! 🎨✨ Beautiful handmade crafts #handmade #crafts #test"
    
    try:
        result = await instagram_service.post_photo(
            image_path=str(test_image),
            caption=caption,
            product_name="Test Product",
            price=500.0
        )
        
        if result["success"]:
            print("✅ Instagram Post - SUCCESS")
            print(f"   Message: {result['message']}")
            if result.get('post_id'):
                print(f"   Post ID: {result['post_id']}")
            return True
        else:
            print("❌ Instagram Post - FAILED")
            print(f"   Error: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Instagram Post - ERROR: {e}")
        return False

async def main():
    """Run Instagram tests"""
    print("🚀 Starting Instagram Service Tests\n")
    
    # Test 1: Connection
    connection_ok = await test_instagram_connection()
    
    # Test 2: Posting (only if connection works)
    posting_ok = False
    if connection_ok:
        posting_ok = await test_instagram_post()
    
    # Summary
    print("\n📊 INSTAGRAM TEST SUMMARY:")
    print(f"   Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"   Photo Upload: {'✅ PASS' if posting_ok else '❌ FAIL'}")
    
    if connection_ok and posting_ok:
        print("\n🎉 ALL TESTS PASSED! Instagram posting is working with your credentials.")
        print("   Your app can now post photos to Instagram automatically!")
    elif connection_ok:
        print("\n⚠️  Connection works but posting failed. Check the error details above.")
    else:
        print("\n❌ Connection failed. Please check your Instagram credentials.")

if __name__ == "__main__":
    asyncio.run(main())
