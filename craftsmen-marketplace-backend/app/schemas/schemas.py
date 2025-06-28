from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    image_url: Optional[str] = None
    ai_generated_caption: Optional[str] = None
    is_active: bool
    facebook_post_id: Optional[str] = None
    instagram_post_id: Optional[str] = None
    created_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True


# Order Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    product: ProductResponse
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True


# Speech Recognition Schema
class SpeechToTextRequest(BaseModel):
    audio_data: str  # Base64 encoded audio data
    language: str = "en-US"


class SpeechToTextResponse(BaseModel):
    text: str
    confidence: float


# AI Caption Generation Schema
class GenerateCaptionRequest(BaseModel):
    product_name: str
    product_description: Optional[str] = None
    price: float
    category: Optional[str] = None


class GenerateCaptionResponse(BaseModel):
    caption: str
    hashtags: List[str]


# Social Media Post Schema
class SocialMediaPostRequest(BaseModel):
    product_id: int
    platforms: List[str] = ["facebook", "instagram"]  # Which platforms to post to


class SocialMediaPostResponse(BaseModel):
    success: bool
    facebook_post_id: Optional[str] = None
    instagram_post_id: Optional[str] = None
    message: str


# File Upload Schema
class FileUploadResponse(BaseModel):
    filename: str
    file_url: str
    file_size: int


# Native Speech Recognition Schemas
class NativeSpeechRequest(BaseModel):
    speech_text: str
    confidence: float = 1.0


class ParsedProductDetails(BaseModel):
    product_name: str
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    confidence: float
