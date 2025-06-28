from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from pydantic import BaseModel

from app.core.database import get_db
from app.services.social_media_automation import SocialMediaAutomationService
from app.models.models import Product

router = APIRouter(prefix="/automation", tags=["social-media-automation"])

# Initialize automation service
automation_service = SocialMediaAutomationService()


class MonitorPostRequest(BaseModel):
    """Request model for monitoring social media posts"""
    product_id: int
    platforms: List[str] = ["facebook", "instagram"]


class DirectMessageRequest(BaseModel):
    """Request model for handling direct messages"""
    message_text: str
    sender_name: str
    sender_platform: str
    sender_id: str


class CommentResponse(BaseModel):
    """Response model for comment automation"""
    comment_text: str
    product_context: str
    platform: str


@router.post("/monitor-post", response_model=Dict[str, Any])
async def monitor_product_post(
    request: MonitorPostRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Monitor a product's social media post for comments and automatically respond
    This runs in the background to continuously monitor interactions
    """
    
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Collect post IDs from different platforms
    post_ids = {}
    if "facebook" in request.platforms and product.facebook_post_id:
        post_ids["facebook"] = product.facebook_post_id
    if "instagram" in request.platforms and product.instagram_post_id:
        post_ids["instagram"] = product.instagram_post_id
    
    if not post_ids:
        raise HTTPException(
            status_code=400, 
            detail="No social media post IDs found for this product"
        )
    
    # Start background monitoring
    background_tasks.add_task(
        automation_service.monitor_and_respond_to_comments,
        post_ids
    )
    
    return {
        "success": True,
        "message": "Background monitoring started for automated responses",
        "product_id": request.product_id,
        "monitoring_platforms": list(post_ids.keys()),
        "post_ids": post_ids
    }


@router.post("/handle-dm", response_model=Dict[str, Any])
async def handle_direct_message(request: DirectMessageRequest):
    """
    Handle direct messages from customers with AI-powered responses
    This endpoint can be called by webhooks from Facebook/Instagram
    """
    
    sender_info = {
        "name": request.sender_name,
        "platform": request.sender_platform,
        "id": request.sender_id
    }
    
    # Generate AI response
    ai_response = await automation_service.handle_direct_message_inquiry(
        message_text=request.message_text,
        sender_info=sender_info
    )
    
    return {
        "success": True,
        "ai_response": ai_response,
        "sender_info": sender_info,
        "original_message": request.message_text,
        "response_type": "direct_message",
        "business_hours": automation_service.is_business_hours()
    }


@router.post("/generate-comment-response", response_model=Dict[str, Any])
async def generate_comment_response(request: CommentResponse):
    """
    Generate an AI response for a specific comment
    Useful for manual review before auto-responding
    """
    
    # Generate response using the automation service
    ai_response = await automation_service._generate_comment_response(
        comment_text=request.comment_text,
        platform=request.platform
    )
    
    return {
        "success": True,
        "original_comment": request.comment_text,
        "ai_response": ai_response,
        "platform": request.platform,
        "product_context": request.product_context
    }


@router.get("/business-status")
async def get_business_status():
    """Get current business status and automation settings"""
    
    from app.core.config import settings
    
    return {
        "business_name": settings.business_name,
        "business_hours": {
            "start": settings.business_hours_start,
            "end": settings.business_hours_end,
            "currently_open": automation_service.is_business_hours()
        },
        "contact_info": {
            "phone": settings.business_phone,
            "email": settings.business_email,
            "location": settings.business_location
        },
        "automation_settings": {
            "auto_respond_comments": settings.auto_respond_to_comments,
            "auto_respond_messages": settings.auto_respond_to_messages
        }
    }


@router.post("/update-business-hours")
async def update_business_hours(
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db)
):
    """Update business hours for automated responses"""
    
    # This would typically update the database
    # For now, we'll just return the new settings
    
    return {
        "success": True,
        "message": "Business hours updated",
        "new_hours": {
            "start": start_time,
            "end": end_time
        }
    }


@router.get("/engagement-stats/{product_id}")
async def get_product_engagement_stats(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get engagement statistics for a product's social media posts"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    stats = {}
    
    # Get Facebook engagement
    if product.facebook_post_id:
        try:
            fb_stats = await automation_service._monitor_facebook_comments(
                product.facebook_post_id
            )
            stats["facebook"] = {
                "post_id": product.facebook_post_id,
                "comments_responded": len(fb_stats),
                "responses": fb_stats
            }
        except Exception as e:
            stats["facebook"] = {"error": str(e)}
    
    # Get Instagram engagement
    if product.instagram_post_id:
        try:
            ig_stats = await automation_service._monitor_instagram_comments(
                product.instagram_post_id
            )
            stats["instagram"] = {
                "post_id": product.instagram_post_id,
                "comments_responded": len(ig_stats),
                "responses": ig_stats
            }
        except Exception as e:
            stats["instagram"] = {"error": str(e)}
    
    return {
        "success": True,
        "product_id": product_id,
        "product_name": product.name,
        "engagement_stats": stats
    }
