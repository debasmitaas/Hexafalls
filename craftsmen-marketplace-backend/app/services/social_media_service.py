import facebook
from instagrapi import Client
from typing import Optional
from app.core.config import settings
from app.schemas.schemas import SocialMediaPostResponse


class SocialMediaService:
    """Service for posting to Facebook and Instagram"""
    
    def __init__(self):
        # Initialize Facebook API
        self.facebook_api = None
        if settings.facebook_access_token:
            self.facebook_api = facebook.GraphAPI(access_token=settings.facebook_access_token)
        
        # Initialize Instagram API
        self.instagram_client = None
        if settings.instagram_access_token:
            self.instagram_client = Client()
    
    async def post_to_social_media(
        self, 
        image_path: str, 
        caption: str, 
        platforms: list = ["facebook", "instagram"]
    ) -> SocialMediaPostResponse:
        """
        Post content to specified social media platforms
        
        Args:
            image_path: Path to the product image
            caption: Caption for the post
            platforms: List of platforms to post to
            
        Returns:
            SocialMediaPostResponse with success status and post IDs
        """
        facebook_post_id = None
        instagram_post_id = None
        messages = []
        
        # Post to Facebook
        if "facebook" in platforms:
            try:
                facebook_post_id = await self._post_to_facebook(image_path, caption)
                if facebook_post_id:
                    messages.append("Posted to Facebook successfully")
                else:
                    messages.append("Failed to post to Facebook")
            except Exception as e:
                messages.append(f"Facebook error: {str(e)}")
        
        # Post to Instagram
        if "instagram" in platforms:
            try:
                instagram_post_id = await self._post_to_instagram(image_path, caption)
                if instagram_post_id:
                    messages.append("Posted to Instagram successfully")
                else:
                    messages.append("Failed to post to Instagram")
            except Exception as e:
                messages.append(f"Instagram error: {str(e)}")
        
        success = bool(facebook_post_id or instagram_post_id)
        message = "; ".join(messages)
        
        return SocialMediaPostResponse(
            success=success,
            facebook_post_id=facebook_post_id,
            instagram_post_id=instagram_post_id,
            message=message
        )
    
    async def _post_to_facebook(self, image_path: str, caption: str) -> Optional[str]:
        """Post to Facebook Page"""
        if not self.facebook_api:
            return None
        
        try:
            # Upload photo to Facebook
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
        if not self.instagram_client:
            return None
        
        try:
            # Upload photo to Instagram
            media = self.instagram_client.photo_upload(
                path=image_path,
                caption=caption
            )
            
            return str(media.pk)
            
        except Exception as e:
            print(f"Instagram posting error: {str(e)}")
            return None
    
    async def get_post_engagement(self, post_id: str, platform: str) -> dict:
        """
        Get engagement metrics for a post
        
        Args:
            post_id: ID of the post
            platform: Platform (facebook or instagram)
            
        Returns:
            Dictionary with engagement metrics
        """
        try:
            if platform == "facebook" and self.facebook_api:
                post_data = self.facebook_api.get_object(
                    id=post_id,
                    fields='likes.summary(true),comments.summary(true),shares'
                )
                
                return {
                    'likes': post_data.get('likes', {}).get('summary', {}).get('total_count', 0),
                    'comments': post_data.get('comments', {}).get('summary', {}).get('total_count', 0),
                    'shares': post_data.get('shares', {}).get('count', 0)
                }
            
            elif platform == "instagram" and self.instagram_client:
                media_info = self.instagram_client.media_info(int(post_id))
                
                return {
                    'likes': media_info.like_count,
                    'comments': media_info.comment_count,
                    'shares': 0  # Instagram doesn't provide share count via API
                }
            
            return {'likes': 0, 'comments': 0, 'shares': 0}
            
        except Exception as e:
            print(f"Error getting engagement for {platform}: {str(e)}")
            return {'likes': 0, 'comments': 0, 'shares': 0}
    
    async def respond_to_comment(self, post_id: str, comment_id: str, response_text: str, platform: str) -> bool:
        """
        Respond to a comment on a post
        
        Args:
            post_id: ID of the post
            comment_id: ID of the comment to respond to
            response_text: Response text
            platform: Platform (facebook or instagram)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if platform == "facebook" and self.facebook_api:
                self.facebook_api.put_comment(
                    object_id=comment_id,
                    message=response_text
                )
                return True
            
            elif platform == "instagram" and self.instagram_client:
                self.instagram_client.media_comment(
                    media_id=int(post_id),
                    text=response_text
                )
                return True
            
            return False
            
        except Exception as e:
            print(f"Error responding to comment on {platform}: {str(e)}")
            return False
