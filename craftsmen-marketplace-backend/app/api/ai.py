from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.schemas.schemas import GenerateCaptionResponse

router = APIRouter()
ai_service = AIService()

class CaptionRequest(BaseModel):
    product_name: str
    price: float = None
    description: str = None
    category: str = None

@router.get("/test")
async def test_ai_service():
    """Test endpoint to debug AI service"""
    try:
        print(f"🔍 AI Service Model: {ai_service.model is not None}")
        print(f"🔍 Has Model: {hasattr(ai_service, 'model')}")
        if ai_service.model:
            print("✅ Gemini model is configured")
        else:
            print("❌ Gemini model is NOT configured")
        
        return {
            "model_configured": ai_service.model is not None,
            "status": "AI service test complete"
        }
    except Exception as e:
        print(f"❌ Test error: {e}")
        return {"error": str(e)}

@router.post("/generate-caption", response_model=GenerateCaptionResponse)
async def generate_caption(request: CaptionRequest):
    """Generate an AI caption for a product based on name and price"""
    
    try:
        caption_response = await ai_service.generate_product_caption(
            product_name=request.product_name,
            product_description=request.description,
            price=request.price,  # Already a float from the model
            category=request.category
        )
        
        return caption_response
        
    except Exception as e:
        # Return a fallback caption if AI generation fails
        price_text = f"{request.price} taka" if request.price else "best price"
        fallback_caption = f"Take this beautiful {request.product_name} ✨ only for {price_text}! Perfect choice 💎 DM for more info 📩"
        
        return GenerateCaptionResponse(
            caption=fallback_caption,
            hashtags=["#handmade", "#craftsmanship", "#beautiful", "#affordable", "#quality"]
        )
