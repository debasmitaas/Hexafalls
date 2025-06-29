import google.generativeai as genai
from typing import List
from app.core.config import settings
from app.schemas.schemas import GenerateCaptionResponse


class AIService:
    """Service for AI-powered caption generation using Google Gemini"""
    
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
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
            print("🚨 USING FALLBACK: Gemini model not configured!")
            price_text = f"{price} rupees" if price else "best price"
            return GenerateCaptionResponse(
                caption=f"Take this beautiful {product_name} ✨ only for {price_text}! DM for more info 📩",
                hashtags=["#handmade", "#craftsmanship", "#beautiful", "#affordable", "#quality"]
            )
        
        try:
            # Create a prompt for caption generation
            prompt = self._create_caption_prompt(product_name, product_description, price, category)
            print(f"🤖 Using Gemini AI for: {product_name} - {price} rupees")
            
            # Generate content using Gemini with higher creativity
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,  # Higher temperature for more creativity
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=200,
                )
            )
            
            print(f"✅ Gemini Response: {response.text[:100]}...")
            
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
            print(f"❌ Error generating caption: {str(e)}")
            print(f"🔄 Using fallback for: {product_name}")
            # Return fallback caption
            price_text = f"{price} rupees" if price else "best price"
            return GenerateCaptionResponse(
                caption=f"Grab this stunning {product_name} ✨ only for {price_text}! Perfect for you 💎 DM for more info 📩",
                hashtags=["#handmade", "#craftsmanship", "#beautiful", "#affordable", "#quality"]
            )
    
    def _create_caption_prompt(self, name: str, description: str, price: float, category: str) -> str:
        """Create a prompt for caption generation"""
        
        prompt = f"""
        Write a ready-to-post social media caption for this handcrafted product:

        Product: {name}
        """
        
        if description:
            prompt += f"Description: {description}\n"
        
        if price:
            prompt += f"Price: {price} rupees\n"
            
        if category:
            prompt += f"Category: {category}\n"
        
        prompt += f"""
        
        CRITICAL INSTRUCTIONS:
        - Write ONLY the caption text that can be directly posted
        - DO NOT write "Here are some ideas" or "Here's a caption" 
        - DO NOT give suggestions or options
        - Write ONE complete, ready-to-use caption
        - MUST include the EXACT price: {price} rupees (not [Price] or placeholder)
        - MUST include "DM to order" or "DM us to order" in the caption
        - Include emojis naturally in the text
        - End with relevant hashtags (at least 5 hashtags)
        - Make it engaging and sales-focused
        - Keep it under 280 characters
        - Use Bangladeshi/local context
        - Be direct and persuasive
        
        Example format: "Amazing handcrafted [product]! ✨ Only {price} rupees! Perfect for [use case] 💖 DM to order now! #handmade #bangladesh #crafts #quality #affordable"
        
        Write the caption now:
        """
        
        return prompt
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from the generated text"""
        import re
        
        # Find all hashtags in the text
        hashtags = re.findall(r'#\w+', text)
        
        # If no hashtags found, add relevant default ones
        if not hashtags:
            hashtags = ["#handmade", "#crafts", "#bangladesh", "#supportlocalwork", "#quality", "#affordable", "#beautiful"]
        
        return hashtags
    
    def _clean_caption(self, text: str) -> str:
        """Clean up the caption text"""
        import re
        
        # Remove any intro phrases like "Here's a caption:" etc.
        text = re.sub(r'^(Here\'s a caption|Here are some ideas|Caption idea|Suggested caption).*?:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^(Here\'s|Here are).*?:', '', text, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and newlines
        text = ' '.join(text.split())
        
        # Return the full text including hashtags - we want everything together
        return text.strip()
    
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
