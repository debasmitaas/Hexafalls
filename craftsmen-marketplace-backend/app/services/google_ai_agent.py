"""
Simple Gemini AI Integration for Craftsmen Marketplace
Clean, working implementation for caption generation
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
import google.generativeai as genai

from app.core.config import settings


class GoogleAIAgent:
    """
    Simple AI Agent using Google Gemini for caption generation
    """
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def generate_enhanced_content(
        self,
        product_name: str,
        price: float,
        category: Optional[str] = None,
        description: Optional[str] = None,
        target_audience: Optional[str] = None,
        platform: str = "both"
    ) -> Dict[str, Any]:
        """
        Generate enhanced content using Gemini
        """
        try:
            # Create the prompt
            prompt = f"""
            Create a compelling social media caption for this handmade product:
            
            Product: {product_name}
            Price: ${price}
            Category: {category or 'handmade crafts'}
            Description: {description or 'Beautiful handmade item'}
            Target Audience: {target_audience or 'craft enthusiasts'}
            
            Requirements:
            - Write an engaging, authentic caption
            - Include emotional storytelling
            - Highlight craftsmanship and uniqueness
            - Add a subtle call-to-action
            - Keep it natural, not overly promotional
            - Make it suitable for both Instagram and Facebook
            
            Also generate 10-12 relevant hashtags including:
            - Product-specific hashtags
            - Craft/handmade hashtags
            - Trending hashtags
            - Community hashtags
            
            Format your response as:
            CAPTION: [your caption here]
            HASHTAGS: [comma-separated hashtags with # symbols]
            """
            
            # Generate content with Gemini
            response = self.model.generate_content(prompt)
            content_text = response.text
            
            # Parse the response
            caption = ""
            hashtags = []
            
            lines = content_text.split('\n')
            for line in lines:
                if line.startswith('CAPTION:'):
                    caption = line.replace('CAPTION:', '').strip()
                elif line.startswith('HASHTAGS:'):
                    hashtag_text = line.replace('HASHTAGS:', '').strip()
                    hashtags = [tag.strip() for tag in hashtag_text.split(',') if tag.strip()]
            
            # Fallback if parsing fails
            if not caption:
                caption = content_text.strip()
            if not hashtags:
                hashtags = ["#handmade", "#crafts", "#artisan", "#supportlocal", "#uniquegifts"]
            
            # Create platform-specific content
            instagram_content = f"{caption}\n\n{' '.join(hashtags[:12])}"
            facebook_content = f"{caption}\n\n{' '.join(hashtags[:8])}"
            
            return {
                "base_caption": caption,
                "hashtags": hashtags,
                "platform_content": {
                    "instagram": instagram_content,
                    "facebook": facebook_content
                },
                "marketing_insights": {
                    "generated_at": datetime.now().isoformat(),
                    "model": "gemini-2.0-flash",
                    "platform": platform
                },
                "metadata": {
                    "product_name": product_name,
                    "price": price,
                    "generated_at": datetime.now().isoformat(),
                    "agent_version": "1.0.0-simple"
                }
            }
            
        except Exception as e:
            # Fallback content
            return {
                "base_caption": f"Check out this amazing {product_name}! Handcrafted with love and attention to detail. Perfect for anyone who appreciates quality craftsmanship. 💫",
                "hashtags": ["#handmade", "#crafts", "#artisan", "#supportlocal", "#uniquegifts"],
                "platform_content": {
                    "instagram": f"Check out this amazing {product_name}! ✨ #handmade #crafts #artisan",
                    "facebook": f"Check out this amazing {product_name}! Handcrafted with love. #handmade #crafts"
                },
                "marketing_insights": {"error": str(e)},
                "metadata": {
                    "product_name": product_name,
                    "price": price,
                    "generated_at": datetime.now().isoformat(),
                    "agent_version": "1.0.0-fallback"
                }
            }
    
    async def analyze_content_performance(self, content: str) -> Dict[str, Any]:
        """
        Analyze content performance potential
        """
        try:
            prompt = f"""
            Analyze this social media content for effectiveness:
            "{content}"
            
            Rate and provide feedback on:
            - Engagement potential (1-10)
            - Clarity and appeal
            - Call-to-action strength
            - Target audience fit
            
            Provide a brief analysis and suggestions for improvement.
            """
            
            response = self.model.generate_content(prompt)
            
            return {
                "analysis": response.text,
                "timestamp": datetime.now().isoformat(),
                "model": "gemini-2.0-flash"
            }
            
        except Exception as e:
            return {
                "analysis": f"Content analysis unavailable: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }


# Global agent instance
_ai_agent: Optional[GoogleAIAgent] = None


def get_ai_agent() -> GoogleAIAgent:
    """Get or create the AI agent instance"""
    global _ai_agent
    if _ai_agent is None:
        _ai_agent = GoogleAIAgent()
    return _ai_agent
