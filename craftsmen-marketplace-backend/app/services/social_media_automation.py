import facebook
from instagrapi import Client
from typing import Optional, List, Dict, Any
from datetime import datetime, time
import asyncio
import json

from app.core.config import settings
from app.services.ai_service import AIService
from app.schemas.schemas import SocialMediaPostResponse


class SocialMediaAutomationService:
    """Advanced service for automated social media posting and customer interaction"""
    
    def __init__(self):
        # Initialize Facebook API
        self.facebook_api = None
        if settings.facebook_access_token:
            self.facebook_api = facebook.GraphAPI(access_token=settings.facebook_access_token)
        
        # Initialize Instagram API
        self.instagram_client = None
        if settings.instagram_access_token:
            self.instagram_client = Client()
        
        # Initialize AI service for automated responses
        self.ai_service = AIService()
    
    async def create_and_post_product(
        self, 
        image_path: str, 
        product_name: str,
        price: float,
        description: str = None,
        category: str = None,
        platforms: List[str] = ["facebook", "instagram"]
    ) -> Dict[str, Any]:
        """
        Complete workflow: Generate AI caption and post to social media
        
        Args:
            image_path: Path to the product image
            product_name: Name of the product
            price: Price of the product
            description: Product description
            category: Product category
            platforms: Platforms to post to
            
        Returns:
            Dictionary with post results and IDs
        """
        
        # Step 1: Generate AI caption
        caption_response = await self.ai_service.generate_product_caption(
            product_name=product_name,
            product_description=description,
            price=price,
            category=category
        )
        
        # Step 2: Create full caption with business info and call-to-action
        full_caption = self._create_business_caption(
            ai_caption=caption_response.caption,
            hashtags=caption_response.hashtags,
            price=price
        )
        
        # Step 3: Post to selected platforms
        post_results = await self._post_to_platforms(
            image_path=image_path,
            caption=full_caption,
            platforms=platforms
        )
        
        return {
            "success": True,
            "ai_caption": caption_response.caption,
            "full_caption": full_caption,
            "hashtags": caption_response.hashtags,
            "post_results": post_results,
            "platforms_posted": platforms
        }
    
    def _create_business_caption(self, ai_caption: str, hashtags: List[str], price: float) -> str:
        """Create a complete business caption with call-to-action"""
        
        cta_text = f"""
        
💰 Price: ${price}
📱 Interested? Send us a DM or comment below!
📞 Contact: {settings.business_phone}
📧 Email: {settings.business_email}
📍 Location: {settings.business_location}

#handmade #craftsmanship #artisan #supportlocal #smallbusiness
        """
        
        hashtags_text = " ".join(hashtags)
        return f"{ai_caption}\n{cta_text}\n{hashtags_text}"
    
    async def _post_to_platforms(
        self, 
        image_path: str, 
        caption: str, 
        platforms: List[str]
    ) -> Dict[str, Any]:
        """Post to multiple social media platforms"""
        
        results = {}
        
        if "facebook" in platforms and self.facebook_api:
            try:
                fb_result = await self._post_to_facebook(image_path, caption)
                results["facebook"] = {
                    "success": fb_result is not None,
                    "post_id": fb_result,
                    "message": "Posted successfully" if fb_result else "Failed to post"
                }
            except Exception as e:
                results["facebook"] = {
                    "success": False,
                    "post_id": None,
                    "message": f"Error: {str(e)}"
                }
        
        if "instagram" in platforms and self.instagram_client:
            try:
                ig_result = await self._post_to_instagram(image_path, caption)
                results["instagram"] = {
                    "success": ig_result is not None,
                    "post_id": ig_result,
                    "message": "Posted successfully" if ig_result else "Failed to post"
                }
            except Exception as e:
                results["instagram"] = {
                    "success": False,
                    "post_id": None,
                    "message": f"Error: {str(e)}"
                }
        
        return results
    
    async def _post_to_facebook(self, image_path: str, caption: str) -> Optional[str]:
        """Post to Facebook Page"""
        try:
            with open(image_path, 'rb') as image_file:
                response = self.facebook_api.put_photo(
                    image=image_file,
                    message=caption
                )
            return response.get('id')
        except Exception as e:
            print(f"Facebook posting error: {str(e)}")
            return None
    
    async def _post_to_instagram(self, image_path: str, caption: str) -> Optional[str]:
        """Post to Instagram Business Account"""
        try:
            media = self.instagram_client.photo_upload(
                path=image_path,
                caption=caption
            )
            return str(media.pk)
        except Exception as e:
            print(f"Instagram posting error: {str(e)}")
            return None
    
    async def monitor_and_respond_to_comments(self, post_ids: Dict[str, str]) -> Dict[str, Any]:
        """
        Monitor posts for new comments and respond automatically
        
        Args:
            post_ids: Dictionary with platform names as keys and post IDs as values
            
        Returns:
            Summary of automated responses
        """
        
        if not settings.auto_respond_to_comments:
            return {"message": "Auto-response disabled"}
        
        responses = {}
        
        # Monitor Facebook comments
        if "facebook" in post_ids and self.facebook_api:
            fb_responses = await self._monitor_facebook_comments(post_ids["facebook"])
            responses["facebook"] = fb_responses
        
        # Monitor Instagram comments
        if "instagram" in post_ids and self.instagram_client:
            ig_responses = await self._monitor_instagram_comments(post_ids["instagram"])
            responses["instagram"] = ig_responses
        
        return responses
    
    async def _monitor_facebook_comments(self, post_id: str) -> List[Dict[str, Any]]:
        """Monitor and respond to Facebook comments"""
        responses = []
        
        try:
            # Get comments on the post
            comments = self.facebook_api.get_object(
                id=post_id,
                fields='comments{id,message,from}'
            ).get('comments', {}).get('data', [])
            
            for comment in comments:
                # Generate AI response
                ai_response = await self._generate_comment_response(
                    comment['message'],
                    platform="facebook"
                )
                
                # Post reply
                try:
                    self.facebook_api.put_comment(
                        object_id=comment['id'],
                        message=ai_response
                    )
                    
                    responses.append({
                        "comment_id": comment['id'],
                        "original_comment": comment['message'],
                        "ai_response": ai_response,
                        "success": True
                    })
                except Exception as e:
                    responses.append({
                        "comment_id": comment['id'],
                        "error": str(e),
                        "success": False
                    })
        
        except Exception as e:
            print(f"Error monitoring Facebook comments: {str(e)}")
        
        return responses
    
    async def _monitor_instagram_comments(self, post_id: str) -> List[Dict[str, Any]]:
        """Monitor and respond to Instagram comments"""
        responses = []
        
        try:
            # Get comments on the post
            comments = self.instagram_client.media_comments(int(post_id))
            
            for comment in comments:
                # Generate AI response
                ai_response = await self._generate_comment_response(
                    comment.text,
                    platform="instagram"
                )
                
                # Post reply
                try:
                    self.instagram_client.media_comment(
                        media_id=int(post_id),
                        text=f"@{comment.user.username} {ai_response}"
                    )
                    
                    responses.append({
                        "comment_id": str(comment.pk),
                        "original_comment": comment.text,
                        "ai_response": ai_response,
                        "success": True
                    })
                except Exception as e:
                    responses.append({
                        "comment_id": str(comment.pk),
                        "error": str(e),
                        "success": False
                    })
        
        except Exception as e:
            print(f"Error monitoring Instagram comments: {str(e)}")
        
        return responses
    
    async def _generate_comment_response(self, comment_text: str, platform: str) -> str:
        """Generate appropriate AI response for comments"""
        
        # Business context for AI
        business_context = f"""
        Business: {settings.business_name}
        Location: {settings.business_location}
        Phone: {settings.business_phone}
        Email: {settings.business_email}
        
        We are craftsmen who create handmade products. 
        We take custom orders and ship nationwide.
        """
        
        # Check if comment contains keywords for common inquiries
        comment_lower = comment_text.lower()
        
        if any(word in comment_lower for word in ["price", "cost", "how much"]):
            return await self.ai_service.generate_comment_response(
                comment_text,
                business_context + "\nCustomer is asking about pricing."
            )
        
        elif any(word in comment_lower for word in ["order", "buy", "purchase", "want"]):
            return f"Thank you for your interest! 😊 Please send us a DM or call {settings.business_phone} to place your order. We'd love to create something special for you! 🎨"
        
        elif any(word in comment_lower for word in ["ship", "delivery", "location"]):
            return f"We ship nationwide! 📦 For shipping details, please DM us or contact {settings.business_phone}. Based in {settings.business_location}. 🚚"
        
        elif any(word in comment_lower for word in ["custom", "personalize", "modify"]):
            return "We love creating custom pieces! ✨ Please DM us with your ideas and we'll work together to create something unique just for you! 🎨"
        
        else:
            # Generic friendly response
            return await self.ai_service.generate_comment_response(
                comment_text,
                business_context
            )
    
    def is_business_hours(self) -> bool:
        """Check if current time is within business hours"""
        now = datetime.now().time()
        start_time = time.fromisoformat(settings.business_hours_start)
        end_time = time.fromisoformat(settings.business_hours_end)
        
        return start_time <= now <= end_time
    
    async def handle_direct_message_inquiry(self, message_text: str, sender_info: Dict[str, Any]) -> str:
        """
        Handle direct messages with AI-powered responses for order inquiries
        
        Args:
            message_text: The message content
            sender_info: Information about the sender
            
        Returns:
            AI-generated response
        """
        
        if not self.is_business_hours():
            return f"""
            Thank you for your message! 🌙 
            
            We're currently outside business hours ({settings.business_hours_start} - {settings.business_hours_end}).
            We'll get back to you as soon as possible during business hours.
            
            For urgent inquiries, please call {settings.business_phone}.
            
            Thanks for your patience! ✨
            """
        
        # Generate contextual response
        business_context = f"""
        You are a customer service representative for {settings.business_name}.
        We create handmade crafts and take custom orders.
        
        Business Details:
        - Phone: {settings.business_phone}
        - Email: {settings.business_email}
        - Location: {settings.business_location}
        
        Customer sent this message: "{message_text}"
        
        Provide a helpful, friendly response. If they're asking about ordering,
        guide them through the process. If they need specific details, 
        encourage them to call or provide contact information.
        """
        
        return await self.ai_service.generate_comment_response(
            message_text,
            business_context
        )
    
    async def create_and_post_product_with_content(
        self, 
        image_path: str, 
        product_name: str,
        price: float,
        description: str = None,
        category: str = None,
        platforms: List[str] = ["facebook", "instagram"],
        ai_caption: str = None,
        platform_content: Dict[str, str] = None,
        hashtags: List[str] = None
    ) -> Dict[str, Any]:
        """
        Enhanced workflow: Use pre-generated AI content and post to social media
        
        Args:
            image_path: Path to the product image
            product_name: Name of the product
            price: Price of the product
            description: Product description
            category: Product category
            platforms: Platforms to post to
            ai_caption: Pre-generated AI caption
            platform_content: Platform-specific content
            hashtags: Pre-generated hashtags
            
        Returns:
            Dictionary with posting results and automation setup
        """
        
        # Use provided content or generate fallback
        caption = ai_caption or f"Check out this amazing {product_name}! Handcrafted with love and attention to detail. Perfect for anyone who appreciates quality craftsmanship. Price: ${price}"
        
        # Use platform-specific content if available
        instagram_caption = platform_content.get("instagram", caption) if platform_content else caption
        facebook_caption = platform_content.get("facebook", caption) if platform_content else caption
        
        # Add hashtags if provided
        if hashtags:
            hashtag_text = " " + " ".join(hashtags)
            if not instagram_caption.endswith(hashtag_text):
                instagram_caption += hashtag_text
            if not facebook_caption.endswith(hashtag_text):
                facebook_caption += hashtag_text
        
        results = {
            "success": True,
            "ai_caption": caption,
            "platform_captions": {
                "instagram": instagram_caption,
                "facebook": facebook_caption
            },
            "post_results": {},
            "automation_enabled": False
        }
        
        # Post to platforms
        if "facebook" in platforms:
            facebook_result = await self.post_to_facebook(
                caption=facebook_caption,
                image_path=image_path
            )
            results["post_results"]["facebook"] = facebook_result
            
            # Enable automated responses
            if facebook_result.get("success") and facebook_result.get("post_id"):
                await self.setup_facebook_automation(
                    post_id=facebook_result["post_id"],
                    product_name=product_name,
                    price=price
                )
                results["automation_enabled"] = True
        
        if "instagram" in platforms:
            instagram_result = await self.post_to_instagram(
                caption=instagram_caption,
                image_path=image_path
            )
            results["post_results"]["instagram"] = instagram_result
            
            # Enable automated responses
            if instagram_result.get("success") and instagram_result.get("post_id"):
                await self.setup_instagram_automation(
                    post_id=instagram_result["post_id"],
                    product_name=product_name,
                    price=price
                )
                results["automation_enabled"] = True
        
        return results

    async def post_to_facebook(self, caption: str, image_path: str) -> Dict[str, Any]:
        """Post to Facebook with enhanced result format"""
        try:
            if not self.facebook_api:
                return {"success": False, "message": "Facebook API not configured", "post_id": None}
            
            with open(image_path, 'rb') as image_file:
                response = self.facebook_api.put_photo(
                    image=image_file,
                    message=caption
                )
            
            post_id = response.get('id')
            return {
                "success": True,
                "post_id": post_id,
                "message": "Posted successfully to Facebook"
            }
        except Exception as e:
            return {
                "success": False,
                "post_id": None,
                "message": f"Facebook posting error: {str(e)}"
            }
    
    async def post_to_instagram(self, caption: str, image_path: str) -> Dict[str, Any]:
        """Post to Instagram with enhanced result format"""
        try:
            if not self.instagram_client:
                return {"success": False, "message": "Instagram API not configured", "post_id": None}
            
            media = self.instagram_client.photo_upload(
                path=image_path,
                caption=caption
            )
            
            post_id = str(media.pk)
            return {
                "success": True,
                "post_id": post_id,
                "message": "Posted successfully to Instagram"
            }
        except Exception as e:
            return {
                "success": False,
                "post_id": None,
                "message": f"Instagram posting error: {str(e)}"
            }
    
    async def setup_facebook_automation(self, post_id: str, product_name: str, price: float):
        """Setup Facebook automation for a specific post"""
        # This would set up monitoring for the specific post
        # For now, it's a placeholder
        print(f"Setting up Facebook automation for post {post_id}")
        pass
    
    async def setup_instagram_automation(self, post_id: str, product_name: str, price: float):
        """Setup Instagram automation for a specific post"""
        # This would set up monitoring for the specific post
        # For now, it's a placeholder
        print(f"Setting up Instagram automation for post {post_id}")
        pass
