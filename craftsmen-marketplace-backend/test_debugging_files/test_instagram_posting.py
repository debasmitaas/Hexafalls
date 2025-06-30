#!/usr/bin/env python3
"""
Test Instagram posting functionality using instagrapi
"""

import asyncio
import sys
import os
sys.path.append(os.getcwd())

from app.services.instagram_service import InstagramService
from app.core.config import settings


async def test_instagram_service():
    """Test Instagram service with instagrapi"""
    
    print("🧪 Testing Instagram Service with instagrapi")
    print(f"📱 Instagram Username: {settings.instagram_username}")
    print(f"🔐 Instagram Password: {'*' * len(settings.instagram_password) if settings.instagram_password else 'Not set'}")
    
    # Initialize Instagram service
    instagram_service = InstagramService()
    
    if not instagram_service.client:
        print("❌ Instagram client not initialized - check credentials in .env file")
        return
    
    print("✅ Instagram client initialized successfully")
    
    # Test login
    print("\n🔐 Testing Instagram login...")
    login_success = instagram_service.login()
    
    if login_success:
        print("✅ Instagram login successful!")
        
        # Test getting user info
        print("\n👤 Getting user info...")
        user_info = instagram_service.get_user_info()
        if "error" not in user_info:
            print(f"✅ User info retrieved: {user_info.get('username', 'N/A')}")
        else:
            print(f"⚠️ User info error: {user_info['error']}")
        
        # Test posting (comment this out if you don't want to actually post)
        # test_image_path = "uploads/test_image.jpg"  # Make sure this file exists
        # if os.path.exists(test_image_path):
        #     print(f"\n📸 Testing photo upload...")
        #     caption = "Test post from our craftsmen marketplace! 🎨 #handmade #test"
        #     result = await instagram_service.post_photo(test_image_path, caption, "Test Product", 100)
        #     if result["success"]:
        #         print(f"✅ Photo posted successfully! Post ID: {result['post_id']}")
        #     else:
        #         print(f"❌ Photo posting failed: {result['error']}")
        
        print("\n📤 Testing logout...")
        instagram_service.logout()
        print("✅ Instagram logout successful!")
        
    else:
        print("❌ Instagram login failed!")
        print("Check your username and password in the .env file")


if __name__ == "__main__":
    asyncio.run(test_instagram_service())
