from instagrapi import Client
from typing import Optional, Dict, Any
from app.core.config import settings
import os
import logging

logger = logging.getLogger(__name__)


class InstagramService:
    """Service for posting to Instagram using instagrapi (latest)"""
    
    def __init__(self):
        self.client = None
        self.is_logged_in = False
        
        # Initialize Instagram client if credentials are provided
        if settings.instagram_username and settings.instagram_password:
            try:
                self.client = Client()
                logger.info(f"🔧 Instagram client initialized for user: {settings.instagram_username}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Instagram client: {e}")
                self.client = None
        else:
            logger.warning("⚠️ Instagram credentials not provided in settings")
    
    def login(self) -> bool:
        """Login to Instagram"""
        if not self.client:
            logger.error("❌ Instagram client not initialized")
            return False
        
        try:
            logger.info(f"🔐 Attempting Instagram login for: {settings.instagram_username}")
            
            login_result = self.client.login(
                settings.instagram_username,
                settings.instagram_password
            )
            
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
    
    def logout(self):
        """Logout from Instagram"""
        if self.client and self.is_logged_in:
            try:
                self.client.logout()
                self.is_logged_in = False
                logger.info("📤 Instagram logout successful")
            except Exception as e:
                logger.error(f"❌ Instagram logout error: {e}")
    
    async def post_photo(
        self, 
        image_path: str, 
        caption: str,
        product_name: str = None,
        price: float = None
    ) -> Dict[str, Any]:
        """
        Post a photo to Instagram using instagrapi
        
        Args:
            image_path: Path to the image file
            caption: Caption for the post
            product_name: Name of the product (optional)
            price: Price of the product (optional)
            
        Returns:
            Dict with success status and post details
        """
        
        if not self.client:
            return {
                "success": False,
                "error": "Instagram client not initialized - check credentials",
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
            
            # Upload photo with caption using instagrapi
            media = self.client.photo_upload(
                path=image_path,
                caption=caption
            )
            
            if media:
                logger.info("✅ Photo posted to Instagram successfully!")
                
                return {
                    "success": True,
                    "message": "Photo posted successfully to Instagram",
                    "post_id": str(media.pk),
                    "media_id": str(media.id), 
                    "username": settings.instagram_username,
                    "media_url": media.thumbnail_url if hasattr(media, 'thumbnail_url') else None
                }
            else:
                logger.error("❌ Failed to upload photo to Instagram")
                return {
                    "success": False,
                    "error": "Upload failed - media object is None",
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
        if not self.client or not self.is_logged_in:
            return {"error": "Client not logged in"}
        
        try:
            target_username = username or settings.instagram_username
            user_info = self.client.user_info_by_username(target_username)
            return user_info.dict() if hasattr(user_info, 'dict') else user_info
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {"error": str(e)}
    
    def get_recent_posts(self, count: int = 10) -> list:
        """Get recent posts from the account"""
        if not self.client or not self.is_logged_in:
            return []
        
        try:
            user_id = self.client.user_id_from_username(settings.instagram_username)
            medias = self.client.user_medias(user_id, amount=count)
            
            posts = []
            for media in medias:
                post_data = {
                    "id": str(media.pk),
                    "caption": media.caption_text,
                    "like_count": media.like_count,
                    "comment_count": media.comment_count,
                    "media_type": media.media_type,
                    "taken_at": media.taken_at,
                }
                posts.append(post_data)
            
            return posts
        except Exception as e:
            logger.error(f"Error getting recent posts: {e}")
            return []
        finally:
            # Logout after posting (optional - you might want to keep the session)
            # self.logout()
            pass
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Instagram connection"""
        if not self.client:
            return {
                "connected": False,
                "error": "Instagram client not initialized",
                "username": None
            }

        if not self.is_logged_in:
            login_success = self.login()
            if not login_success:
                return {
                    "connected": False,
                    "error": "Failed to login",
                    "username": settings.instagram_username
                }

        return {
            "connected": True,
            "message": "Instagram connection successful",
            "username": settings.instagram_username
        }


# Create a global instance
instagram_service = InstagramService()
