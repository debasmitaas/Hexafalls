from InstagramAPI import InstagramAPI
from typing import Optional, Dict, Any
from app.core.config import settings
import os
import logging

logger = logging.getLogger(__name__)


class InstagramService:
    """Service for posting to Instagram using InstagramAPI"""
    
    def __init__(self):
        self.api = None
        self.is_logged_in = False
        
        # Initialize Instagram API if credentials are provided
        if settings.instagram_username and settings.instagram_password:
            try:
                self.api = InstagramAPI(
                    settings.instagram_username, 
                    settings.instagram_password
                )
                logger.info(f"🔧 Instagram API initialized for user: {settings.instagram_username}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Instagram API: {e}")
                self.api = None
        else:
            logger.warning("⚠️ Instagram credentials not provided in settings")
    
    def login(self) -> bool:
        """Login to Instagram"""
        if not self.api:
            logger.error("❌ Instagram API not initialized")
            return False
        
        try:
            login_result = self.api.login()
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
        if self.api and self.is_logged_in:
            try:
                self.api.logout()
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
        Post a photo to Instagram
        
        Args:
            image_path: Path to the image file
            caption: Caption for the post
            product_name: Name of the product (optional)
            price: Price of the product (optional)
            
        Returns:
            Dict with success status and post details
        """
        
        if not self.api:
            return {
                "success": False,
                "error": "Instagram API not initialized - check credentials",
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
            
            # Upload photo with caption
            result = self.api.uploadPhoto(image_path, caption=caption)
            
            if result:
                logger.info("✅ Photo posted to Instagram successfully!")
                
                # Try to get the post ID (this might not always be available)
                post_id = None
                try:
                    # The InstagramAPI might store the last media ID
                    if hasattr(self.api, 'LastJson') and self.api.LastJson:
                        post_id = self.api.LastJson.get('media', {}).get('id', None)
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
                error_msg = "Upload failed"
                
                # Try to get error details
                try:
                    if hasattr(self.api, 'LastJson') and self.api.LastJson:
                        error_msg = self.api.LastJson.get('message', 'Upload failed')
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
        finally:
            # Logout after posting (optional - you might want to keep the session)
            # self.logout()
            pass
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Instagram connection"""
        if not self.api:
            return {
                "connected": False,
                "error": "Instagram API not initialized",
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
