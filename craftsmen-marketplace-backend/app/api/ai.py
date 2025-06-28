from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.schemas.schemas import GenerateCaptionResponse

router = APIRouter()
ai_service = AIService()

class CaptionRequest(BaseModel):
    product_name: str
    price: str = None
    description: str = None
    category: str = None

@router.post("/generate-caption", response_model=GenerateCaptionResponse)
async def generate_caption(request: CaptionRequest):
    """Generate an AI caption for a product based on name and price"""
    
    try:
        # Convert price string to float if provided
        price_float = None
        if request.price:
            try:
                # Remove any currency symbols and convert to float
                price_clean = ''.join(filter(str.isdigit, request.price.replace('.', '')))
                price_float = float(price_clean) if price_clean else None
            except:
                price_float = None
        
        caption_response = await ai_service.generate_product_caption(
            product_name=request.product_name,
            product_description=request.description,
            price=price_float,
            category=request.category
        )
        
        return caption_response
        
    except Exception as e:
        # Return a fallback caption if AI generation fails
        fallback_caption = f"🌟 {request.product_name}"
        if request.price:
            fallback_caption += f" - Only {request.price}"
        fallback_caption += " 🌟\n\n#handmade #craftsmen #marketplace #quality"
        
        return GenerateCaptionResponse(
            caption=fallback_caption,
            hashtags=["#handmade", "#craftsmen", "#marketplace", "#quality"]
        )
