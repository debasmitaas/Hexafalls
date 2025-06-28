from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.schemas.schemas import SpeechToTextResponse

router = APIRouter(prefix="/speech", tags=["speech-native"])


class TextInputRequest(BaseModel):
    """Request model for direct text input (from Flutter native speech)"""
    text: str
    confidence: float = 1.0
    language: str = "en-US"


class ParseSpeechRequest(BaseModel):
    """Request model for parsing speech text into product details"""
    speech_text: str


class ParsedProductDetails(BaseModel):
    """Response model for parsed product details"""
    product_name: str
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    confidence: float


@router.post("/process-native-speech", response_model=ParsedProductDetails)
async def process_native_speech_text(
    request: ParseSpeechRequest,
    db: Session = Depends(get_db)
):
    """
    Process speech text from Flutter native speech recognition
    Parse it into structured product details using simple text processing
    """
    
    try:
        speech_text = request.speech_text.lower().strip()
        
        # Initialize result
        result = ParsedProductDetails(
            product_name="",
            price=None,
            description=None,
            category=None,
            confidence=0.8
        )
        
        # Parse price from speech text
        price = _extract_price_from_text(speech_text)
        if price:
            result.price = price
        
        # Parse product name and description
        product_info = _extract_product_info(speech_text)
        result.product_name = product_info.get("name", "")
        result.description = product_info.get("description", "")
        result.category = _guess_category(speech_text)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing speech text: {str(e)}"
        )


def _extract_price_from_text(text: str) -> Optional[float]:
    """Extract price from speech text"""
    import re
    
    # Look for patterns like "25 dollars", "$25", "twenty five dollars"
    price_patterns = [
        r'\$(\d+(?:\.\d{2})?)',  # $25.99
        r'(\d+(?:\.\d{2})?) dollars?',  # 25.99 dollars
        r'(\d+) bucks?',  # 25 bucks
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except:
                continue
    
    # Handle spoken numbers (basic implementation)
    number_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
        'twenty-five': 25, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100
    }
    
    words = text.split()
    for i, word in enumerate(words):
        if word in number_words and i + 1 < len(words) and 'dollar' in words[i + 1]:
            return float(number_words[word])
    
    return None


def _extract_product_info(text: str) -> dict:
    """Extract product name and description from text"""
    
    # Remove price-related words
    price_words = ['dollar', 'dollars', 'buck', 'bucks', '$']
    words = text.split()
    filtered_words = [w for w in words if not any(p in w for p in price_words)]
    
    # Remove numbers that are likely prices
    import re
    filtered_words = [w for w in filtered_words if not re.match(r'^\d+(\.\d{2})?$', w)]
    
    # Common craft-related keywords for better parsing
    craft_keywords = [
        'handmade', 'handcrafted', 'wooden', 'ceramic', 'pottery', 'jewelry',
        'necklace', 'bracelet', 'ring', 'bowl', 'vase', 'sculpture', 'painting',
        'carved', 'painted', 'woven', 'knitted', 'embroidered'
    ]
    
    # Find main product words
    product_words = []
    description_words = []
    
    for word in filtered_words:
        if word in craft_keywords or len(word) > 4:  # Likely product-related
            product_words.append(word)
        else:
            description_words.append(word)
    
    # Build product name (first few meaningful words)
    product_name = ' '.join(product_words[:3]) if product_words else ' '.join(filtered_words[:3])
    
    # Build description
    description = ' '.join(filtered_words) if len(filtered_words) > 3 else None
    
    return {
        "name": product_name.title(),
        "description": description.capitalize() if description else None
    }


def _guess_category(text: str) -> Optional[str]:
    """Guess product category from speech text"""
    
    categories = {
        'jewelry': ['jewelry', 'necklace', 'bracelet', 'ring', 'earring', 'pendant'],
        'pottery': ['pottery', 'ceramic', 'bowl', 'vase', 'mug', 'plate', 'clay'],
        'woodwork': ['wooden', 'wood', 'carved', 'furniture', 'cutting board'],
        'textiles': ['fabric', 'woven', 'knitted', 'embroidered', 'scarf', 'blanket'],
        'art': ['painting', 'drawing', 'artwork', 'canvas', 'sculpture'],
        'home decor': ['decoration', 'decorative', 'home', 'ornament']
    }
    
    text_lower = text.lower()
    
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            return category.title()
    
    return "Handmade"  # Default category


@router.post("/validate-speech-text", response_model=dict)
async def validate_speech_text(request: TextInputRequest):
    """Simple endpoint to validate and clean speech text from Flutter"""
    
    return {
        "original_text": request.text,
        "cleaned_text": request.text.strip(),
        "confidence": request.confidence,
        "language": request.language,
        "word_count": len(request.text.split()),
        "has_price": _extract_price_from_text(request.text.lower()) is not None
    }
