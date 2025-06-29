#!/usr/bin/env python3
"""
Test the combined Instagram + Gemini AI service
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.instagram_gemini_service import instagram_gemini_service
    from app.core.config import settings
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the backend directory")
    sys.exit(1)


async def test_service_configuration():
    """Test if both services are properly configured"""
    print("🔍 Testing Service Configuration...")
    
    test_result = instagram_gemini_service.test_services()
    
    print(f"   Gemini AI: {'✅ Configured' if test_result['gemini_configured'] else '❌ Not configured'}")
    print(f"   Instagram API: {'✅ Configured' if test_result['instagram_configured'] else '❌ Not configured'}")
    print(f"   Instagram Login: {'✅ Success' if test_result['instagram_login'] else '❌ Failed'}")
    print(f"   Services Ready: {'✅ Ready' if test_result['services_ready'] else '❌ Not ready'}")
    
    return test_result['services_ready']


async def test_ai_caption_generation():
    """Test AI caption generation"""
    print("\n🤖 Testing AI Caption Generation...")
    
    try:
        caption_result = await instagram_gemini_service.generate_caption_with_gemini(
            product_name="Handmade Ceramic Bowl",
            price=750.0,
            description="Beautiful blue ceramic bowl with traditional patterns",
            category="pottery"
        )
        
        if caption_result['ai_generated']:
            print("✅ AI Caption Generation - SUCCESS")
            print(f"   Caption: {caption_result['caption'][:100]}...")
            print(f"   Hashtags: {', '.join(caption_result['hashtags'][:5])}...")
            print(f"   AI Generated: {caption_result['ai_generated']}")
        else:
            print("⚠️ AI Caption Generation - FALLBACK USED")
            print(f"   Fallback Caption: {caption_result['caption'][:100]}...")
            if 'error' in caption_result:
                print(f"   Error: {caption_result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Caption Generation - ERROR: {e}")
        return False


async def test_instagram_posting():
    """Test posting to Instagram with AI caption"""
    print("\n📸 Testing Complete Instagram Posting Workflow...")
    
    # Find a test image
    uploads_dir = Path("uploads")
    test_images = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.png")) + list(uploads_dir.glob("*.JPG"))
    
    if not test_images:
        print("❌ No test images found in uploads directory")
        print("   Please add a test image to the uploads folder")
        return False
    
    test_image = test_images[0]
    print(f"   Using image: {test_image.name}")
    
    try:
        # Post with AI-generated caption
        result = await instagram_gemini_service.post_to_instagram_with_ai_caption(
            image_path=str(test_image),
            product_name="Test Handmade Product",
            price=500.0,
            description="Beautiful handcrafted item for testing",
            category="handicrafts"
        )
        
        print(f"   Caption Generated: {'✅' if result['caption_generated'] else '❌'}")
        print(f"   Instagram Posted: {'✅' if result['instagram_posted'] else '❌'}")
        
        if result['success']:
            print("✅ Complete Workflow - SUCCESS")
            print(f"   AI Caption: {result['ai_caption'][:100]}...")
            print(f"   Hashtags: {', '.join(result['hashtags'][:3])}...")
            if result['post_id']:
                print(f"   Post ID: {result['post_id']}")
            return True
        else:
            print("❌ Complete Workflow - FAILED")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Instagram Posting Workflow - ERROR: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Testing Instagram + Gemini AI Service\n")
    
    # Test 1: Service configuration
    config_ok = await test_service_configuration()
    
    # Test 2: AI caption generation
    caption_ok = await test_ai_caption_generation()
    
    # Test 3: Complete Instagram posting (only if config is OK)
    posting_ok = False
    if config_ok:
        posting_ok = await test_instagram_posting()
    else:
        print("\n⚠️ Skipping Instagram posting test due to configuration issues")
    
    # Summary
    print("\n📊 TEST SUMMARY:")
    print(f"   Service Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   AI Caption Generation: {'✅ PASS' if caption_ok else '❌ FAIL'}")
    print(f"   Instagram Posting: {'✅ PASS' if posting_ok else '❌ FAIL'}")
    
    if config_ok and caption_ok and posting_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("   Your Instagram + Gemini AI service is fully functional!")
        print("   You can now automatically generate AI captions and post to Instagram!")
    elif caption_ok:
        print("\n⚠️ AI caption generation works, but Instagram posting needs attention.")
        print("   Check your Instagram credentials and try again.")
    else:
        print("\n❌ Some services need configuration.")
        print("   Check your .env file for Gemini API key and Instagram credentials.")


if __name__ == "__main__":
    asyncio.run(main())
