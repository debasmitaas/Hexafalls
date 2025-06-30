from instabot import Bot
from typing import List, Optional, Dict, Any
from app.core.config import settings
import os
import logging

logger = logging.getLogger(__name__)


class InstagramService:
    """Service for posting to Instagram using instabot"""
    
    def __init__(self):
        self.bot = None
        self.is_logged_in = False
        
        # Initialize Instagram bot if credentials are provided
        if settings.instagram_username and settings.instagram_password:
            try:
                self.bot = Bot()
                logger.info(f"🔧 Instagram bot initialized for user: {settings.instagram_username}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Instagram bot: {e}")
                self.bot = None
        else:
            logger.warning("⚠️ Instagram credentials not provided in settings")
    
    def login(self) -> bool:
        """Login to Instagram with persistent session"""
        if not self.bot:
            logger.error("❌ Instagram bot not initialized")
            return False

        # If already logged in, just return True
        if self.is_logged_in:
            logger.info("✅ Already logged in to Instagram")
            return True

        try:
            # Try to login with stored session first
            login_result = self.bot.login(
                username=settings.instagram_username,
                password=settings.instagram_password,
                use_cookie=True  # Use saved session if available
            )
            if login_result:
                self.is_logged_in = True
                logger.info("✅ Instagram login successful - session will stay active")
                return True
            else:
                logger.error("❌ Instagram login failed")
                return False
        except Exception as e:
            logger.error(f"❌ Instagram login error: {e}")
            # If login fails, try without cookie
            try:
                login_result = self.bot.login(
                    username=settings.instagram_username,
                    password=settings.instagram_password,
                    use_cookie=False
                )
                if login_result:
                    self.is_logged_in = True
                    logger.info("✅ Instagram login successful (retry) - session will stay active")
                    return True
            except Exception as retry_error:
                logger.error(f"❌ Instagram login retry failed: {retry_error}")
            return False
    
    def logout(self):
        """Logout from Instagram - DISABLED to keep session active"""
        # Keep the session active for automatic posting
        logger.info("� Keeping Instagram session active for automatic posting")
        pass  # Don't actually logout
    
    async def post_photo(
        self, 
        image_path: str, 
        caption: str,
        product_name: str = None,
        price: float = None
    ) -> Dict[str, Any]:
        """
        Post a photo to Instagram
        
        Args:
            image_path: Path to the image file
            caption: Caption for the post
            product_name: Name of the product (optional)
            price: Price of the product (optional)
            
        Returns:
            Dict with success status and post details
        """
        
        if not self.bot:
            return {
                "success": False,
                "error": "Instagram bot not initialized - check credentials",
                "post_id": None
            }
        
        # Check if image file exists
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image file not found: {image_path}",
                "post_id": None
            }
        
        # Login if not already logged in
        if not self.is_logged_in:
            if not self.login():
                return {
                    "success": False,
                    "error": "Failed to login to Instagram",
                    "post_id": None
                }
        
        try:
            logger.info(f"📸 Posting to Instagram: {product_name} - {image_path}")
            logger.info(f"📝 Caption: {caption[:100]}...")
            
            # Upload photo with caption using instabot
            result = self.bot.upload_photo(image_path, caption=caption)
            
            if result:
                logger.info("✅ Photo posted to Instagram successfully!")
                
                # Try to get the post ID
                post_id = None
                try:
                    # Get the last uploaded media ID
                    if hasattr(self.bot, 'last_media_id') and self.bot.last_media_id:
                        post_id = str(self.bot.last_media_id)
                        logger.info(f"📱 Instagram Post ID: {post_id}")
                except:
                    pass
                
                return {
                    "success": True,
                    "message": "Photo posted successfully to Instagram",
                    "post_id": post_id,
                    "username": settings.instagram_username
                }
            else:
                logger.error("❌ Failed to upload photo to Instagram")
                return {
                    "success": False,
                    "error": "Upload failed - check image format and caption",
                    "post_id": None
                }
                
        except Exception as e:
            logger.error(f"❌ Instagram posting error: {e}")
            return {
                "success": False,
                "error": f"Instagram posting error: {str(e)}",
                "post_id": None
            }
    
    def get_user_info(self, username: str = None) -> Dict[str, Any]:
        """Get user information"""
        if not self.bot or not self.is_logged_in:
            return {"error": "Bot not logged in"}
        
        try:
            target_username = username or settings.instagram_username
            user_id = self.bot.get_user_id_from_username(target_username)
            user_info = self.bot.get_user_info(user_id)
            return user_info
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {"error": str(e)}
    
    def get_recent_posts(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent posts from the account"""
        if not self.bot or not self.is_logged_in:
            return []
        
        try:
            user_id = self.bot.get_user_id_from_username(settings.instagram_username)
            media_ids = self.bot.get_user_medias(user_id, filtration=False)[:count]
            
            posts = []
            for media_id in media_ids:
                media_info = self.bot.get_media_info(media_id)
                posts.append(media_info)
            
            return posts
        except Exception as e:
            logger.error(f"Error getting recent posts: {e}")
            return []
