from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
import uuid
from PIL import Image

from app.core.database import get_db
from app.models.models import Product, User
from app.schemas.schemas import (
    ProductCreate, ProductResponse, ProductUpdate,
    GenerateCaptionRequest, GenerateCaptionResponse,
    SocialMediaPostRequest, SocialMediaPostResponse,
    FileUploadResponse
)
from app.services.ai_service import AIService
from app.services.social_media_automation import SocialMediaAutomationService
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


@router.post("/create-and-post", response_model=Dict[str, Any])
async def create_product_and_auto_post(
    image_file: UploadFile = File(...),
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    owner_id: int = Form(...),
    platforms: List[str] = Form(["facebook", "instagram"]),
    db: Session = Depends(get_db)
):
    """
    Complete workflow: Upload image, create product, generate AI caption, 
    and auto-post to social media with business automation
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
    
    # Get full image path for social media posting
    image_path = os.path.join(settings.upload_folder, image_upload.filename)
    
    # Use advanced social media automation
    automation_result = await social_automation.create_and_post_product(
        image_path=image_path,
        product_name=name,
        price=price,
        description=description,
        category=category,
        platforms=platforms
    )
    
    # Update product with social media post IDs
    post_results = automation_result.get("post_results", {})
    if post_results.get("facebook", {}).get("post_id"):
        db_product.facebook_post_id = post_results["facebook"]["post_id"]
    if post_results.get("instagram", {}).get("post_id"):
        db_product.instagram_post_id = post_results["instagram"]["post_id"]
    
    # Store AI-generated caption
    db_product.ai_generated_caption = automation_result.get("ai_caption", "")
    
    db.commit()
    db.refresh(db_product)
    
    return {
        "success": True,
        "product": ProductResponse.from_orm(db_product),
        "automation_result": automation_result,
        "message": "Product created and posted to social media with automated business responses enabled"
    }


@router.get("/", response_model=List[ProductResponse])
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
    return [ProductResponse.from_orm(product) for product in products]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse.from_orm(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return ProductResponse.from_orm(product)


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (soft delete)"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
    
    return {"message": "Product deleted successfully"}


@router.post("/{product_id}/generate-caption", response_model=GenerateCaptionResponse)
async def generate_product_caption(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Generate a new AI caption for a product"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    caption_response = await ai_service.generate_product_caption(
        product_name=product.name,
        product_description=product.description,
        price=product.price,
        category=product.category
    )
    
    # Update product with new caption
    product.ai_generated_caption = caption_response.caption
    db.commit()
    
    return caption_response


@router.post("/{product_id}/post-to-social", response_model=Dict[str, Any])
async def post_product_to_social_media(
    product_id: int,
    platforms: List[str] = ["facebook", "instagram"],
    db: Session = Depends(get_db)
):
    """Post an existing product to social media platforms with business automation"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.image_url:
        raise HTTPException(status_code=400, detail="Product has no image")
    
    # Construct full image path
    filename = product.image_url.split('/')[-1]
    image_path = os.path.join(settings.upload_folder, filename)
    
    # Use advanced social media automation
    automation_result = await social_automation.create_and_post_product(
        image_path=image_path,
        product_name=product.name,
        price=product.price,
        description=product.description,
        category=product.category,
        platforms=platforms
    )
    
    # Update product with social media post IDs
    post_results = automation_result.get("post_results", {})
    if post_results.get("facebook", {}).get("post_id"):
        product.facebook_post_id = post_results["facebook"]["post_id"]
    if post_results.get("instagram", {}).get("post_id"):
        product.instagram_post_id = post_results["instagram"]["post_id"]
    
    # Update AI-generated caption
    product.ai_generated_caption = automation_result.get("ai_caption", "")
    
    db.commit()
    
    return {
        "success": True,
        "product_id": product_id,
        "automation_result": automation_result,
        "message": "Product posted to social media with automated business responses enabled"
    }
