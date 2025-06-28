from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "Craftsmen Marketplace API"
    version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./craftsmen_marketplace.db"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Cloud
    google_cloud_project: Optional[str] = None
    google_application_credentials: Optional[str] = None
    
    # Gemini AI
    gemini_api_key: Optional[str] = None
    
    # Facebook API
    facebook_app_id: Optional[str] = None
    facebook_app_secret: Optional[str] = None
    facebook_access_token: Optional[str] = None
    
    # Instagram API
    instagram_business_account_id: Optional[str] = None
    instagram_access_token: Optional[str] = None
    
    # File Upload
    upload_folder: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = ["jpg", "jpeg", "png", "gif"]
    
    # Social Media Automation
    auto_respond_to_comments: bool = True
    auto_respond_to_messages: bool = True
    business_hours_start: str = "09:00"
    business_hours_end: str = "18:00"
    
    # Business Information for AI Responses
    business_name: str = "Your Craft Business Name"
    business_location: str = "Your City, State"
    business_phone: str = "+1234567890"
    business_email: str = "orders@yourcraft.com"
    
    class Config:
        env_file = ".env"


settings = Settings()
