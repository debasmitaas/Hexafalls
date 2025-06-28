import google.generativeai as genai
from typing import List
from app.core.config import settings
from app.schemas.schemas import GenerateCaptionResponse


class AIService:
    """Service for AI-powered caption generation using Google Gemini"""
    
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def generate_product_caption(
        self, 
        product_name: str, 
        product_description: str = None, 
        price: float = None,
        category: str = None
    ) -> GenerateCaptionResponse:
        """
        Generate an engaging caption for a product using Gemini AI
        
        Args:
            product_name: Name of the product
            product_description: Description of the product
            price: Price of the product
            category: Category of the product
            
        Returns:
            GenerateCaptionResponse with caption and hashtags
        """
        if not self.model:
            # Fallback caption if AI is not configured
            return GenerateCaptionResponse(
                caption=f"Check out this amazing {product_name}! Handcrafted with love and attention to detail. ${price if price else 'Contact for pricing'}",
                hashtags=["#handmade", "#craftsmanship", "#artisan", "#unique", "#quality"]
            )
        
        try:
            # Create a prompt for caption generation
            prompt = self._create_caption_prompt(product_name, product_description, price, category)
            
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            caption_text = response.text.strip()
            
            # Extract hashtags (assuming they're at the end of the caption)
            hashtags = self._extract_hashtags(caption_text)
            
            # Clean caption (remove hashtags from the main text)
            clean_caption = self._clean_caption(caption_text)
            
            return GenerateCaptionResponse(
                caption=clean_caption,
                hashtags=hashtags
            )
            
        except Exception as e:
            print(f"Error generating caption: {str(e)}")
            # Return fallback caption
            return GenerateCaptionResponse(
                caption=f"Beautiful {product_name} - handcrafted with passion! ${price if price else 'Contact for pricing'}",
                hashtags=["#handmade", "#craftsmanship", "#artisan"]
            )
    
    def _create_caption_prompt(self, name: str, description: str, price: float, category: str) -> str:
        """Create a prompt for caption generation"""
        prompt = f"""
        Create an engaging social media caption for a handcrafted product with the following details:
        
        Product Name: {name}
        """
        
        if description:
            prompt += f"Description: {description}\n"
        
        if price:
            prompt += f"Price: ${price}\n"
            
        if category:
            prompt += f"Category: {category}\n"
        
        prompt += """
        Requirements:
        1. Write a captivating caption that highlights the craftsmanship and uniqueness
        2. Include relevant hashtags at the end
        3. Keep it engaging and authentic
        4. Emphasize the handmade quality
        5. Include a call-to-action
        6. Maximum 280 characters
        
        Format the response as a single caption with hashtags included.
        """
        
        return prompt
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from the generated text"""
        words = text.split()
        hashtags = [word for word in words if word.startswith('#')]
        
        # If no hashtags found, add default ones
        if not hashtags:
            hashtags = ["#handmade", "#craftsmanship", "#artisan", "#unique"]
        
        return hashtags
    
    def _clean_caption(self, text: str) -> str:
        """Remove hashtags from the main caption text"""
        words = text.split()
        clean_words = [word for word in words if not word.startswith('#')]
        return ' '.join(clean_words).strip()
    
    async def generate_comment_response(self, original_comment: str, product_context: str) -> str:
        """
        Generate automated responses to comments
        
        Args:
            original_comment: The comment to respond to
            product_context: Context about the product
            
        Returns:
            Generated response text
        """
        if not self.model:
            return "Thank you for your interest! Please DM us for more details."
        
        try:
            prompt = f"""
            Generate a friendly and professional response to this customer comment about a handcrafted product:
            
            Customer Comment: "{original_comment}"
            Product Context: {product_context}
            
            Requirements:
            1. Be friendly and professional
            2. Answer any questions if possible
            3. Encourage engagement
            4. Keep it concise (under 100 characters)
            5. Include a call-to-action if appropriate
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating comment response: {str(e)}")
            return "Thank you for your comment! Feel free to message us for more information. 😊"
