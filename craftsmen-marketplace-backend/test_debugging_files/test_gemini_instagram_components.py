#!/usr/bin/env python3
"""
Test Gemini AI caption generation specifically
"""

import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
    import google.generativeai as genai
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


async def test_gemini_caption_generation():
    """Test Gemini AI caption generation directly"""
    print("🤖 Testing Gemini AI Caption Generation...")
    
    # Check if Gemini is configured
    if not settings.gemini_api_key:
        print("❌ Gemini API key not found in settings")
        return False
    
    try:
        # Initialize Gemini
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        print("✅ Gemini AI initialized successfully")
        
        # Create Instagram-optimized prompt
        product_name = "Handmade Wooden Bowl"
        price = 450.0
        description = "Beautiful carved wooden bowl with traditional design"
        category = "handicrafts"
        
        prompt = f"""Create an engaging Instagram caption for a handmade product:

Product: {product_name}
Price: ₹{price}
Description: {description}
Category: {category}

Requirements:
- 2-3 lines, engaging and enthusiastic
- Use relevant emojis
- Include call-to-action (DM for orders)
- Add 8-10 relevant hashtags
- Keep it Instagram-friendly

Generate the caption:"""
        
        print("🤖 Generating caption...")
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95,
                top_k=40,
                max_output_tokens=300,
            )
        )
        
        caption = response.text.strip()
        
        print("✅ Caption generated successfully!")
        print("📝 Generated Caption:")
        print("-" * 50)
        print(caption)
        print("-" * 50)
        
        # Extract hashtags
        import re
        hashtags = re.findall(r'#\w+', caption)
        print(f"🏷️ Found {len(hashtags)} hashtags: {', '.join(hashtags[:5])}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini caption generation failed: {e}")
        return False


async def test_instagram_credentials():
    """Test Instagram credentials without posting"""
    print("\n🔍 Testing Instagram Credentials...")
    
    if not settings.instagram_username or not settings.instagram_password:
        print("❌ Instagram credentials not found in settings")
        return False
    
    print(f"   Username: {settings.instagram_username}")
    print(f"   Password: {'*' * len(settings.instagram_password)}")
    
    # Try to import and initialize (without logging in)
    try:
        from InstagramAPI import InstagramAPI
        api = InstagramAPI(settings.instagram_username, settings.instagram_password)
        print("✅ Instagram API initialized successfully")
        return True
    except ImportError:
        print("❌ InstagramAPI module not found")
        return False
    except Exception as e:
        print(f"❌ Instagram API initialization failed: {e}")
        return False


async def main():
    """Run tests"""
    print("🚀 Testing Gemini AI + Instagram Components\n")
    
    # Test 1: Gemini caption generation
    gemini_ok = await test_gemini_caption_generation()
    
    # Test 2: Instagram credentials
    instagram_ok = await test_instagram_credentials()
    
    # Summary
    print(f"\n📊 COMPONENT TEST SUMMARY:")
    print(f"   Gemini AI: {'✅ WORKING' if gemini_ok else '❌ FAILED'}")
    print(f"   Instagram Setup: {'✅ READY' if instagram_ok else '❌ FAILED'}")
    
    if gemini_ok and instagram_ok:
        print("\n🎉 Both components are working!")
        print("   Ready to integrate Instagram posting with AI captions!")
    elif gemini_ok:
        print("\n⚠️ Gemini AI works, but Instagram needs attention.")
    elif instagram_ok:
        print("\n⚠️ Instagram setup works, but Gemini AI needs attention.")
    else:
        print("\n❌ Both components need configuration.")


if __name__ == "__main__":
    asyncio.run(main())
