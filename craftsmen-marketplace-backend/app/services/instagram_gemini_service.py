"""
Complete Instagram posting service with Gemini AI caption generation
"""

from InstagramAPI import InstagramAPI
from typing import Optional, Dict, Any, List
from app.core.config import settings
import google.generativeai as genai
import os
import logging
import asyncio

logger = logging.getLogger(__name__)


class InstagramGeminiService:
    """Service for AI-powered Instagram posting using Gemini and InstagramAPI"""
    
    def __init__(self):
        # Initialize Instagram API
        self.instagram_api = None
        self.is_logged_in = False
        
        # Initialize Gemini AI
        self.gemini_model = None
        
        self._initialize_instagram()
        self._initialize_gemini()
    
    def _initialize_instagram(self):
        """Initialize Instagram API"""
        if settings.instagram_username and settings.instagram_password:
            try:
                self.instagram_api = InstagramAPI(
                    settings.instagram_username, 
                    settings.instagram_password
                )
                logger.info(f"🔧 Instagram API initialized for user: {settings.instagram_username}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Instagram API: {e}")
                self.instagram_api = None
        else:
            logger.warning("⚠️ Instagram credentials not provided in settings")
    
    def _initialize_gemini(self):
        """Initialize Gemini AI"""
        if settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("🤖 Gemini AI initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini AI: {e}")
                self.gemini_model = None
        else:
            logger.warning("⚠️ Gemini API key not provided in settings")
    
    def login_instagram(self) -> bool:
        """Login to Instagram"""
        if not self.instagram_api:
            logger.error("❌ Instagram API not initialized")
            return False
        
        try:
            login_result = self.instagram_api.login()
            if login_result:
                self.is_logged_in = True
                logger.info("✅ Instagram login successful")
                return True
            else:
                logger.error("❌ Instagram login failed")
                return False
        except Exception as e:
            logger.error(f"❌ Instagram login error: {e}")
            return False
    
    async def generate_caption_with_gemini(
        self, 
        product_name: str, 
        price: float = None,
        description: str = None,
        category: str = None
    ) -> Dict[str, Any]:
        """
        Generate Instagram caption using Gemini AI
        
        Args:
            product_name: Name of the product
            price: Price of the product
            description: Product description
            category: Product category
            
        Returns:
            Dict with caption and hashtags
        """
        
        if not self.gemini_model:
            # Fallback caption if Gemini is not available
            price_text = f"₹{price}" if price else "great price"
            return {
                "caption": f"✨ Beautiful {product_name} available now! Only {price_text} 🛍️ DM for orders 📩",
                "hashtags": ["#handmade", "#crafts", "#beautiful", "#affordable", "#instagram"],
                "ai_generated": False,
                "fallback_used": True
            }
        
        try:
            # Create detailed prompt for Instagram-specific caption
            prompt = self._create_instagram_caption_prompt(product_name, price, description, category)
            
            logger.info(f"🤖 Generating caption with Gemini for: {product_name}")
            
            # Generate caption with Gemini
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,  # High creativity for engaging content
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=300,
                )
            )
            
            caption_text = response.text.strip()
            logger.info(f"✅ Gemini caption generated: {caption_text[:100]}...")
            
            # Extract hashtags and clean caption
            hashtags = self._extract_hashtags(caption_text)
            clean_caption = self._clean_caption(caption_text)
            
            return {
                "caption": clean_caption,
                "hashtags": hashtags,
                "ai_generated": True,
                "fallback_used": False,
                "full_response": caption_text
            }
            
        except Exception as e:
            logger.error(f"❌ Gemini caption generation failed: {e}")
            # Return fallback caption
            price_text = f"₹{price}" if price else "great price"
            return {
                "caption": f"✨ Stunning {product_name} now available! Get yours for {price_text} 🎨 DM us! 📩",
                "hashtags": ["#handmade", "#crafts", "#beautiful", "#affordable", "#art"],
                "ai_generated": False,
                "fallback_used": True,
                "error": str(e)
            }
    
    def _create_instagram_caption_prompt(self, name: str, price: float, description: str, category: str) -> str:
        """Create optimized prompt for Instagram captions"""
        
        prompt = f"""Create an engaging Instagram caption for a handmade product. Make it vibrant, appealing, and Instagram-friendly.

Product Details:
- Name: {name}
- Price: ₹{price if price else 'Contact for price'}
- Description: {description or 'Beautiful handcrafted item'}
- Category: {category or 'handmade crafts'}

Requirements:
1. Write an engaging, enthusiastic caption (2-3 lines max)
2. Use relevant emojis naturally
3. Include a clear call-to-action (DM, WhatsApp, etc.)
4. Add 8-12 relevant hashtags at the end
5. Make it sound authentic and personal
6. Appeal to craft lovers and art enthusiasts
7. Mention the price naturally
8. Keep it concise but impactful

Style: Friendly, enthusiastic, authentic, Instagram-native

Example format:
✨ [Engaging description with emojis] 🎨
Perfect for [use case]! Only ₹{price} 💕
DM for orders 📩

#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5 #hashtag6 #hashtag7 #hashtag8

Generate the caption now:"""
        
        return prompt
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from caption text"""
        import re
        hashtags = re.findall(r'#\w+', text)
        return hashtags[:12]  # Limit to 12 hashtags
    
    def _clean_caption(self, text: str) -> str:
        """Remove hashtags from main caption text"""
        import re
        # Remove hashtags but keep the rest
        lines = text.split('\n')
        clean_lines = []
        
        for line in lines:
            # If line is mostly hashtags, skip it
            if line.count('#') > 2 and len(line.replace('#', '').replace(' ', '')) < 20:
                continue
            clean_lines.append(line)
        
        return '\n'.join(clean_lines).strip()
    
    async def post_to_instagram_with_ai_caption(
        self,
        image_path: str,
        product_name: str,
        price: float = None,
        description: str = None,
        category: str = None,
        custom_caption: str = None
    ) -> Dict[str, Any]:
        """
        Complete workflow: Generate AI caption and post to Instagram
        
        Args:
            image_path: Path to the image file
            product_name: Name of the product
            price: Price of the product
            description: Product description
            category: Product category
            custom_caption: Use custom caption instead of AI-generated
            
        Returns:
            Dict with posting results and AI caption details
        """
        
        result = {
            "success": False,
            "instagram_posted": False,
            "caption_generated": False,
            "ai_caption": None,
            "hashtags": [],
            "post_id": None,
            "error": None
        }
        
        try:
            # Step 1: Generate AI caption (unless custom provided)
            if custom_caption:
                caption_data = {
                    "caption": custom_caption,
                    "hashtags": [],
                    "ai_generated": False
                }
            else:
                logger.info("🤖 Generating AI caption...")
                caption_data = await self.generate_caption_with_gemini(
                    product_name, price, description, category
                )
            
            result["caption_generated"] = True
            result["ai_caption"] = caption_data["caption"]
            result["hashtags"] = caption_data["hashtags"]
            
            # Combine caption and hashtags for Instagram
            full_caption = caption_data["caption"]
            if caption_data["hashtags"]:
                hashtag_text = " ".join(caption_data["hashtags"])
                full_caption = f"{caption_data['caption']}\n\n{hashtag_text}"
            
            logger.info(f"📝 Final caption ready: {full_caption[:100]}...")
            
            # Step 2: Post to Instagram
            instagram_result = await self._post_to_instagram(image_path, full_caption, product_name)
            
            result["instagram_posted"] = instagram_result["success"]
            result["post_id"] = instagram_result.get("post_id")
            
            if instagram_result["success"]:
                result["success"] = True
                logger.info("🎉 Complete workflow successful!")
            else:
                result["error"] = instagram_result.get("error", "Instagram posting failed")
                
        except Exception as e:
            logger.error(f"❌ Complete workflow failed: {e}")
            result["error"] = f"Workflow error: {str(e)}"
        
        return result
    
    async def _post_to_instagram(self, image_path: str, caption: str, product_name: str) -> Dict[str, Any]:
        """Post photo to Instagram"""
        
        if not self.instagram_api:
            return {
                "success": False,
                "error": "Instagram API not initialized",
                "post_id": None
            }
        
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image file not found: {image_path}",
                "post_id": None
            }
        
        # Login if not already logged in
        if not self.is_logged_in:
            if not self.login_instagram():
                return {
                    "success": False,
                    "error": "Failed to login to Instagram",
                    "post_id": None
                }
        
        try:
            logger.info(f"📸 Posting to Instagram: {product_name}")
            
            # Upload photo
            result = self.instagram_api.uploadPhoto(image_path, caption=caption)
            
            if result:
                logger.info("✅ Photo posted to Instagram successfully!")
                
                # Try to get post ID
                post_id = None
                try:
                    if hasattr(self.instagram_api, 'LastJson') and self.instagram_api.LastJson:
                        post_id = self.instagram_api.LastJson.get('media', {}).get('id', None)
                except:
                    pass
                
                return {
                    "success": True,
                    "message": "Photo posted successfully to Instagram",
                    "post_id": post_id,
                    "username": settings.instagram_username
                }
            else:
                logger.error("❌ Instagram upload failed")
                error_msg = "Upload failed"
                
                try:
                    if hasattr(self.instagram_api, 'LastJson') and self.instagram_api.LastJson:
                        error_msg = self.instagram_api.LastJson.get('message', error_msg)
                except:
                    pass
                
                return {
                    "success": False,
                    "error": error_msg,
                    "post_id": None
                }
                
        except Exception as e:
            logger.error(f"❌ Instagram posting error: {e}")
            return {
                "success": False,
                "error": f"Instagram posting error: {str(e)}",
                "post_id": None
            }
    
    def test_services(self) -> Dict[str, Any]:
        """Test both Gemini and Instagram services"""
        result = {
            "gemini_configured": self.gemini_model is not None,
            "instagram_configured": self.instagram_api is not None,
            "instagram_login": False,
            "services_ready": False
        }
        
        # Test Instagram login
        if self.instagram_api:
            result["instagram_login"] = self.login_instagram()
        
        result["services_ready"] = (
            result["gemini_configured"] and 
            result["instagram_configured"] and 
            result["instagram_login"]
        )
        
        return result


# Create global instance
instagram_gemini_service = InstagramGeminiService()
