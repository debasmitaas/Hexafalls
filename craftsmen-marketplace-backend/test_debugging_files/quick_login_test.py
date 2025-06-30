#!/usr/bin/env python3
"""
Quick Instagram login test to save session for automatic posting
"""
import sys
import os
sys.path.append('.')

from app.services.instagram_service_new import InstagramService
import asyncio

async def test_login():
    print("🔐 Testing Instagram auto-login...")
    
    # Initialize Instagram service
    insta_service = InstagramService()
    
    if not insta_service.bot:
        print("❌ Instagram bot not initialized - check credentials")
        return False
    
    # Test login
    login_success = insta_service.login()
    
    if login_success:
        print("✅ Instagram login successful! Session saved for automatic posting.")
        print("🚀 Your Flutter app should now be able to post automatically!")
        
        # Test a simple operation to verify the session
        try:
            user_info = insta_service.bot.get_self_info()
            print(f"📱 Logged in as: {user_info.username}")
            print(f"👥 Followers: {user_info.follower_count}")
        except Exception as e:
            print(f"⚠️ Warning: Could not get user info: {e}")
        
        # Logout to clean up
        insta_service.logout()
        return True
    else:
        print("❌ Instagram login failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_login())
    if success:
        print("\n🎉 SUCCESS! Your Instagram integration is ready!")
        print("Try your Flutter app now - it should post automatically!")
    else:
        print("\n💥 FAILED! Check your Instagram credentials in .env file")
