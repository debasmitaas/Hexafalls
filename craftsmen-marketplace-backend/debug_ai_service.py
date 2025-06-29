#!/usr/bin/env python3
"""
Debug AI Service Issues
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from app.services.ai_service import AIService
    from app.core.config import settings
    import google.generativeai as genai
    
    def debug_ai_service():
        print("🔍 Debugging AI Service...")
        
        # Check settings
        print(f"API Key in settings: {'✅ Present' if settings.gemini_api_key else '❌ Missing'}")
        if settings.gemini_api_key:
            print(f"API Key: {settings.gemini_api_key[:15]}...")
        
        # Test direct Gemini API
        print("\n🧪 Testing Direct Gemini API...")
        try:
            genai.configure(api_key=settings.gemini_api_key)
            
            # Try different model names
            model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            working_model = None
            for model_name in model_names:
                try:
                    print(f"   Trying model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    
                    # Simple test
                    response = model.generate_content("Say hello")
                    if response and response.text:
                        print(f"   ✅ {model_name} works!")
                        working_model = model_name
                        break
                    else:
                        print(f"   ❌ {model_name} no response")
                        
                except Exception as e:
                    print(f"   ❌ {model_name} failed: {e}")
                    
            if working_model:
                print(f"\n✅ Working model found: {working_model}")
                return working_model
            else:
                print("\n❌ No working models found")
                return None
                
        except Exception as e:
            print(f"❌ Direct API test failed: {e}")
            return None
    
    def test_ai_service():
        print("\n🔍 Testing AI Service Instance...")
        
        ai_service = AIService()
        
        if ai_service.model:
            print("✅ AI Service model initialized")
        else:
            print("❌ AI Service model NOT initialized")
            return False
        
        try:
            # Test caption generation
            print("\n🧪 Testing caption generation...")
            import asyncio
            
            async def test_caption():
                result = await ai_service.generate_product_caption(
                    product_name="Test Handmade Bowl",
                    product_description="Beautiful ceramic bowl",
                    price=500.0,
                    category="pottery"
                )
                return result
            
            result = asyncio.run(test_caption())
            
            if result and hasattr(result, 'caption'):
                print(f"✅ Caption generated: {result.caption}")
                print(f"✅ Hashtags: {result.hashtags}")
                return True
            else:
                print("❌ No caption generated")
                return False
                
        except Exception as e:
            print(f"❌ Caption generation failed: {e}")
            return False
    
    if __name__ == "__main__":
        print("🚀 AI Service Debugging\n")
        
        # Test 1: Direct API
        working_model = debug_ai_service()
        
        # Test 2: AI Service
        service_ok = test_ai_service()
        
        print(f"\n📊 RESULTS:")
        print(f"   Working Model: {working_model or 'None'}")
        print(f"   AI Service: {'✅ OK' if service_ok else '❌ FAILED'}")
        
        if working_model and not service_ok:
            print(f"\n🔧 RECOMMENDATION: Update ai_service.py to use '{working_model}' instead of 'gemini-pro'")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the backend directory")
