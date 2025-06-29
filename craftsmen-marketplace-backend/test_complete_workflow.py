#!/usr/bin/env python3
"""
Test complete Instagram posting workflow
"""

import asyncio
import sys
import os
sys.path.append(os.getcwd())

from app.services.instagram_service import InstagramService
from app.services.ai_service import AIService
from app.core.config import settings


async def test_complete_workflow():
    """Test the complete Instagram posting workflow"""
    
    print("🧪 Testing Complete Instagram Posting Workflow")
    
    # Step 1: Generate AI caption
    print("\n🤖 Step 1: Generating AI caption...")
    ai_service = AIService()
    
    caption_response = await ai_service.generate_product_caption(
        product_name="Handwoven Basket",
        product_description="Beautiful handwoven basket perfect for home decor",
        price=850,
        category="Home Decor"
    )
    
    print(f"✅ AI Caption Generated:")
    print(f"Caption: {caption_response.caption}")
    print(f"Hashtags: {caption_response.hashtags}")
    
    # Step 2: Test Instagram posting
    print("\n📱 Step 2: Testing Instagram service...")
    instagram_service = InstagramService()
    
    if not instagram_service.client:
        print("❌ Instagram client not initialized")
        return
    
    # Use an existing image from uploads
    test_image_path = "uploads/196c4c70-babe-4eb3-b882-a321ffe11248.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    print(f"📸 Using test image: {test_image_path}")
    
    # Test posting (uncomment to actually post)
    print("\n🚀 Step 3: Testing Instagram posting...")
    print("⚠️  NOTE: This will actually post to Instagram!")
    print("⚠️  Comment out the posting code if you don't want to post")
    
    # UNCOMMENT BELOW TO ACTUALLY POST TO INSTAGRAM
    result = await instagram_service.post_photo(
        image_path=test_image_path,
        caption=caption_response.caption,
        product_name="Handwoven Basket",
        price=850
    )
    
    if result["success"]:
        print(f"✅ Instagram posting successful!")
        print(f"Post ID: {result['post_id']}")
        print(f"Media ID: {result.get('media_id', 'N/A')}")
        print(f"Username: {result['username']}")
    else:
        print(f"❌ Instagram posting failed: {result['error']}")
    
    print("\n🏁 Test completed!")


if __name__ == "__main__":
    asyncio.run(test_complete_workflow())
