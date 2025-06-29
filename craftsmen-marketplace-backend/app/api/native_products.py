from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
import uuid
import json
from PIL import Image

from app.core.database import get_db
from app.models.models import Product
from app.schemas.schemas import ProductResponse, FileUploadResponse
from app.services.ai_service import AIService
from app.services.social_media_automation import SocialMediaAutomationService
from app.services.google_ai_agent import get_ai_agent
from app.core.config import settings

router = APIRouter(prefix="/products", tags=["products"])

# Initialize services
ai_service = AIService()
social_automation = SocialMediaAutomationService()


@router.post("/upload-image", response_model=FileUploadResponse)
async def upload_product_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a product image"""
    
    # Validate file type
    if not file.filename.lower().endswith(tuple(settings.allowed_extensions)):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_extensions)}"
        )
    
    # Check file size
    contents = await file.read()
    if len(contents) > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size too large. Maximum size: {settings.max_file_size / (1024*1024)}MB"
        )
    
    # Create uploads directory if it doesn't exist
    os.makedirs(settings.upload_folder, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(settings.upload_folder, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Optimize image
    try:
        with Image.open(file_path) as img:
            # Resize if too large
            if img.width > 1200 or img.height > 1200:
                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                img.save(file_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Error optimizing image: {str(e)}")
    
    return FileUploadResponse(
        filename=unique_filename,
        file_url=f"/uploads/{unique_filename}",
        file_size=len(contents)
    )


@router.post("/create-and-post-native", response_model=Dict[str, Any])
async def create_product_and_auto_post_native(
    image_file: UploadFile = File(...),
    product_name: str = Form(..., alias="product_name"),  # Accept both name and product_name
    name: Optional[str] = Form(None),  # For backward compatibility
    price: float = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),  # Accept pre-generated caption
    owner_id: int = Form(1),
    platforms: str = Form('["facebook", "instagram"]'),  # JSON string from FlutterFlow
    db: Session = Depends(get_db)
):
    """
    Complete workflow for FlutterFlow: Upload image, create product, 
    generate AI caption with Google ADK, and auto-post to social media
    """
    
    # Handle name field (support both 'name' and 'product_name')
    product_name_value = product_name or name
    if not product_name_value:
        raise HTTPException(status_code=400, detail="Product name is required")
    
    # Upload image first
    image_upload = await upload_product_image(file=image_file, db=db)
    
    # Create product in database
    db_product = Product(
        name=product_name_value,
        description=description,
        price=price,
        category=category,
        image_url=image_upload.file_url,
        owner_id=owner_id
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Get full image path for social media posting
    image_path = os.path.join(settings.upload_folder, image_upload.filename)
    
    # Parse platforms (FlutterFlow sends as JSON string)
    try:
        platforms_list = json.loads(platforms) if isinstance(platforms, str) else platforms
    except:
        platforms_list = ["facebook", "instagram"]  # fallback
    
    # Use enhanced Google AI Agent for caption generation (only if no caption provided)
    if caption:
        # Use the provided caption from frontend
        ai_caption = caption
        platform_content = {
            "instagram": caption,
            "facebook": caption
        }
        hashtags = []  # Extract hashtags from caption if needed
        marketing_insights = {"caption_source": "frontend_preview"}
        
        # Extract hashtags from the provided caption
        import re
        hashtag_matches = re.findall(r'#\w+', caption)
        hashtags = [tag.replace('#', '') for tag in hashtag_matches]
        
    else:
        # Generate new caption using AI
        ai_agent = get_ai_agent()
        
        # Determine platform for optimization
        platform_target = "both"
        if len(platforms_list) == 1:
            platform_target = platforms_list[0]
        
        # Generate enhanced content using Google ADK
        try:
            enhanced_content = await ai_agent.generate_enhanced_content(
                product_name=product_name_value,
                price=price,
                category=category,
                description=description,
                target_audience="craft enthusiasts and art lovers",
                platform=platform_target
            )
            
            # Extract platform-specific content
            platform_content = enhanced_content.get("platform_content", {})
            ai_caption = enhanced_content.get("base_caption", "")
            hashtags = enhanced_content.get("hashtags", [])
            marketing_insights = enhanced_content.get("marketing_insights", {})
            
        except Exception as e:
            print(f"Enhanced AI agent failed, using fallback: {e}")
            # Fallback to basic AI service
            ai_caption_response = await ai_service.generate_product_caption(
                product_name=product_name_value,
                product_description=description or "",
                price=price,
                category=category or "handmade"
            )
            # Extract the actual caption string from the response
            ai_caption = ai_caption_response.caption
            platform_content = {
                "instagram": ai_caption,
                "facebook": ai_caption
            }
            hashtags = ai_caption_response.hashtags
            marketing_insights = {"fallback_used": True}
    
    # Use social media automation with enhanced content
    automation_result = await social_automation.create_and_post_product_with_content(
        image_path=image_path,
        product_name=product_name_value,
        price=price,
        description=description,
        category=category,
        platforms=platforms_list,
        ai_caption=ai_caption,
        platform_content=platform_content,
        hashtags=hashtags
    )
    
    # Update product with social media post IDs and enhanced data
    post_results = automation_result.get("post_results", {})
    if post_results.get("facebook", {}).get("post_id"):
        db_product.facebook_post_id = post_results["facebook"]["post_id"]
    if post_results.get("instagram", {}).get("post_id"):
        db_product.instagram_post_id = post_results["instagram"]["post_id"]
    
    # Store AI-generated caption and insights
    db_product.ai_generated_caption = ai_caption
    
    db.commit()
    db.refresh(db_product)
    
    return {
        "success": True,
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "price": db_product.price,
            "image_url": db_product.image_url,
            "ai_caption": db_product.ai_generated_caption,
            "facebook_post_id": db_product.facebook_post_id,
            "instagram_post_id": db_product.instagram_post_id
        },
        "enhanced_content": {
            "platform_content": platform_content,
            "hashtags": hashtags,
            "marketing_insights": marketing_insights
        },
        "automation_result": automation_result,
        "message": "Product created and posted to social media using enhanced Google ADK AI agent with automated business responses enabled"
    }


@router.get("/", response_model=List[Dict[str, Any]])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    owner_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of products with optional filtering"""
    
    query = db.query(Product).filter(Product.is_active == True)
    
    if category:
        query = query.filter(Product.category == category)
    
    if owner_id:
        query = query.filter(Product.owner_id == owner_id)
    
    products = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "category": product.category,
            "image_url": product.image_url,
            "ai_caption": product.ai_generated_caption,
            "facebook_post_id": product.facebook_post_id,
            "instagram_post_id": product.instagram_post_id,
            "created_at": product.created_at.isoformat() if product.created_at else None
        }
        for product in products
    ]


@router.post("/preview-content", response_model=Dict[str, Any])
async def preview_ai_content(
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    platform: str = Form("both")
):
    """
    Preview AI-generated content using Google ADK before posting
    Perfect for the Flutter frontend preview screen
    """
    
    # Get the enhanced AI agent
    ai_agent = get_ai_agent()
    
    try:
        # Generate enhanced content
        enhanced_content = await ai_agent.generate_enhanced_content(
            product_name=name,
            price=price,
            category=category,
            description=description,
            target_audience="craft enthusiasts and art lovers",
            platform=platform
        )
        
        # Analyze content performance
        base_caption = enhanced_content.get("base_caption", "")
        performance_analysis = await ai_agent.analyze_content_performance(base_caption)
        
        return {
            "success": True,
            "content": enhanced_content,
            "performance_analysis": performance_analysis,
            "preview_data": {
                "instagram_preview": enhanced_content.get("platform_content", {}).get("instagram", base_caption),
                "facebook_preview": enhanced_content.get("platform_content", {}).get("facebook", base_caption),
                "hashtags": enhanced_content.get("hashtags", []),
                "estimated_engagement": "High" if "ADK" in str(enhanced_content.get("metadata", {})) else "Medium"
            },
            "message": "Content preview generated successfully with Google ADK insights"
        }
        
    except Exception as e:
        # Fallback preview
        basic_caption = f"Check out this amazing {name}! Handcrafted with love and attention to detail. Perfect for anyone who appreciates quality craftsmanship. 💫\n\nPrice: ${price}"
        
        return {
            "success": True,
            "content": {
                "base_caption": basic_caption,
                "hashtags": ["#handmade", "#crafts", "#artisan", "#supportlocal"],
                "platform_content": {
                    "instagram": basic_caption + "\n\n#handmade #crafts #artisan",
                    "facebook": basic_caption + "\n\n#handmade #crafts"
                }
            },
            "performance_analysis": {"analysis": "Basic content analysis", "error": str(e)},
            "preview_data": {
                "instagram_preview": basic_caption + "\n\n#handmade #crafts #artisan",
                "facebook_preview": basic_caption + "\n\n#handmade #crafts",
                "hashtags": ["#handmade", "#crafts", "#artisan", "#supportlocal"],
                "estimated_engagement": "Medium"
            },
            "message": "Content preview generated with fallback (Google ADK unavailable)"
        }


@router.post("/post-with-preview", response_model=Dict[str, Any])
async def post_with_previewed_content(
    image_file: UploadFile = File(...),
    name: str = Form(...),
    price: float = Form(...),
    preview_content: str = Form(...),  # JSON string with previewed content
    platforms: str = Form('["facebook", "instagram"]'),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    owner_id: int = Form(1),
    db: Session = Depends(get_db)
):
    """
    Post to social media using content that was previously previewed
    This is for when users approve the preview in Flutter
    """
    
    # Upload image first
    image_upload = await upload_product_image(file=image_file, db=db)
    
    # Create product in database
    db_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        image_url=image_upload.file_url,
        owner_id=owner_id
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Get full image path
    image_path = os.path.join(settings.upload_folder, image_upload.filename)
    
    # Parse platforms and preview content
    try:
        platforms_list = json.loads(platforms) if isinstance(platforms, str) else platforms
        content_data = json.loads(preview_content) if isinstance(preview_content, str) else preview_content
    except:
        platforms_list = ["facebook", "instagram"]
        content_data = {}
    
    # Extract content from preview
    ai_caption = content_data.get("base_caption", f"Check out this amazing {name}!")
    platform_content = content_data.get("platform_content", {})
    hashtags = content_data.get("hashtags", ["#handmade", "#crafts"])
    
    # Post using the previewed content
    automation_result = await social_automation.create_and_post_product_with_content(
        image_path=image_path,
        product_name=name,
        price=price,
        description=description,
        category=category,
        platforms=platforms_list,
        ai_caption=ai_caption,
        platform_content=platform_content,
        hashtags=hashtags
    )
    
    # Update product with results
    post_results = automation_result.get("post_results", {})
    if post_results.get("facebook", {}).get("post_id"):
        db_product.facebook_post_id = post_results["facebook"]["post_id"]
    if post_results.get("instagram", {}).get("post_id"):
        db_product.instagram_post_id = post_results["instagram"]["post_id"]
    
    db_product.ai_generated_caption = ai_caption
    db.commit()
    db.refresh(db_product)
    
    return {
        "success": True,
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "price": db_product.price,
            "image_url": db_product.image_url,
            "ai_caption": db_product.ai_generated_caption,
            "facebook_post_id": db_product.facebook_post_id,
            "instagram_post_id": db_product.instagram_post_id
        },
        "automation_result": automation_result,
        "message": "Product posted successfully using previewed content"
    }
