# Craftsmen Marketplace Backend

A FastAPI-based backend for a craftsmen marketplace app that helps craftsmen showcase their work on social media to earn money. This API integrates with AI services for caption generation, speech-to-text conversion, and automated social media posting.

## 🚀 Features

- **Image Upload & Processing**: Upload and optimize product images
- **Speech-to-Text**: Convert voice input to text for product descriptions
- **AI Caption Generation**: Generate engaging captions using Google Gemini AI
- **Social Media Integration**: Auto-post to Facebook and Instagram
- **Order Management**: Handle product orders and customer information
- **Comment Automation**: AI-powered responses to social media comments
- **Database**: SQLite database for storing products, orders, and user data

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Google Cloud Speech-to-Text**: Voice recognition service
- **Google Gemini AI**: AI content generation
- **Facebook SDK**: Facebook/Instagram API integration
- **Pillow**: Image processing
- **UV**: Fast Python package manager

## 📋 Prerequisites

- Python 3.8+
- UV package manager
- Google Cloud account (for Speech-to-Text API)
- Google AI Studio account (for Gemini API)
- Facebook Developer account (for social media posting)
- Instagram Business account (for Instagram posting)

## 🔧 Installation & Setup

### 1. Clone and Navigate to Project

```bash
cd "f:\flutter app project\craftsmen-marketplace-backend"
```

### 2. Install Dependencies

The dependencies are already installed, but if you need to reinstall:

```bash
uv sync
```

### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

Edit `.env` file with your actual API keys and configuration:

```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Facebook API
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_ACCESS_TOKEN=your-facebook-access-token

# Instagram API
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-instagram-business-account-id
INSTAGRAM_ACCESS_TOKEN=your-instagram-access-token
```

### 4. Run the Application

```bash
uv run python main.py
```

Or using uvicorn directly:

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
craftsmen-marketplace-backend/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py          # Application settings
│   │   └── database.py        # Database configuration
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── schemas.py         # Pydantic schemas
│   ├── services/
│   │   ├── ai_service.py      # AI caption generation
│   │   ├── speech_service.py  # Speech-to-text conversion
│   │   └── social_media_service.py  # Social media posting
│   └── api/
│       ├── products.py        # Product endpoints
│       ├── orders.py          # Order endpoints
│       └── speech.py          # Speech-to-text endpoints
├── uploads/                   # Uploaded images directory
├── main.py                    # FastAPI application entry point
├── pyproject.toml            # Project dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🔗 API Endpoints

### Products
- `POST /api/products/upload-image` - Upload product image
- `POST /api/products/create-with-speech` - Create product with image and speech input
- `GET /api/products/` - Get all products
- `GET /api/products/{id}` - Get specific product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `POST /api/products/{id}/generate-caption` - Generate AI caption
- `POST /api/products/{id}/post-to-social` - Post to social media

### Orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/` - Get all orders
- `GET /api/orders/{id}` - Get specific order
- `PUT /api/orders/{id}` - Update order
- `POST /api/orders/{id}/confirm` - Confirm order
- `POST /api/orders/{id}/complete` - Complete order
- `POST /api/orders/{id}/cancel` - Cancel order

### Speech-to-Text
- `POST /api/speech/text-to-speech` - Convert base64 audio to text
- `POST /api/speech/audio-file-to-text` - Convert audio file to text

## 🔑 API Key Setup Guide

### 1. Google Cloud Speech-to-Text

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Speech-to-Text API
4. Create a service account and download the JSON key file
5. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your JSON key file

### 2. Google Gemini AI

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Set `GEMINI_API_KEY` in your .env file

### 3. Facebook API

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login and Instagram Basic Display products
4. Get your App ID, App Secret, and Access Token
5. Set the respective environment variables

### 4. Instagram API

1. Set up Instagram Business Account
2. Connect it to your Facebook Page
3. Use Facebook Graph API to get Instagram Business Account ID
4. Set `INSTAGRAM_BUSINESS_ACCOUNT_ID` and access token

## 🚀 Usage Examples

### 1. Upload Image and Create Product

```python
import requests

# Upload image
files = {'file': open('product_image.jpg', 'rb')}
response = requests.post('http://localhost:8000/api/products/upload-image', files=files)
print(response.json())

# Create product with speech input
form_data = {
    'name': 'Handmade Ceramic Vase',
    'price': 45.99,
    'description': 'Beautiful handcrafted ceramic vase',
    'category': 'Home Decor',
    'owner_id': 1,
    'auto_post': True
}
files = {'image_file': open('product_image.jpg', 'rb')}
response = requests.post('http://localhost:8000/api/products/create-with-speech', 
                        data=form_data, files=files)
print(response.json())
```

### 2. Speech-to-Text Conversion

```python
import base64
import requests

# Convert audio file to base64
with open('audio_recording.wav', 'rb') as f:
    audio_data = base64.b64encode(f.read()).decode()

# Send to API
payload = {
    'audio_data': audio_data,
    'language': 'en-US'
}
response = requests.post('http://localhost:8000/api/speech/text-to-speech', json=payload)
print(response.json())
```

### 3. Create Order

```python
import requests

order_data = {
    'customer_name': 'John Doe',
    'customer_phone': '+1234567890',
    'customer_email': 'john@example.com',
    'delivery_address': '123 Main St, City, State',
    'items': [
        {
            'product_id': 1,
            'quantity': 2,
            'price': 45.99
        }
    ]
}

response = requests.post('http://localhost:8000/api/orders/', json=order_data)
print(response.json())
```

## 🔄 Integration with Flutter Frontend

### Flutter HTTP Client Setup

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  
  static Future<Map<String, dynamic>> uploadImage(File imageFile) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/products/upload-image'),
    );
    
    request.files.add(
      await http.MultipartFile.fromPath('file', imageFile.path),
    );
    
    var response = await request.send();
    var responseData = await response.stream.toBytes();
    var responseString = String.fromCharCodes(responseData);
    
    return json.decode(responseString);
  }
  
  static Future<Map<String, dynamic>> createProduct({
    required File imageFile,
    required String name,
    required double price,
    String? description,
    String? category,
    required int ownerId,
    bool autoPost = false,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/products/create-with-speech'),
    );
    
    request.files.add(
      await http.MultipartFile.fromPath('image_file', imageFile.path),
    );
    
    request.fields.addAll({
      'name': name,
      'price': price.toString(),
      'owner_id': ownerId.toString(),
      'auto_post': autoPost.toString(),
      if (description != null) 'description': description,
      if (category != null) 'category': category,
    });
    
    var response = await request.send();
    var responseData = await response.stream.toBytes();
    var responseString = String.fromCharCodes(responseData);
    
    return json.decode(responseString);
  }
}
```

## 🛡️ Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **API Keys**: Keep all API keys secure and rotate them regularly
3. **CORS**: Configure CORS properly for production
4. **File Upload**: Implement proper file validation and size limits
5. **Rate Limiting**: Add rate limiting for production use
6. **Authentication**: Implement user authentication for production

## 🚀 Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]
```

### Environment Variables for Production

```env
DEBUG=False
DATABASE_URL=postgresql://user:password@db:5432/craftsmen_marketplace
SECRET_KEY=your-very-secure-secret-key
```

## 📞 Support

For questions and support:

1. Check the [FastAPI Documentation](https://fastapi.tiangolo.com/)
2. Review the [Google Cloud Speech-to-Text API docs](https://cloud.google.com/speech-to-text/docs)
3. Check [Google AI Studio documentation](https://ai.google.dev/docs)
4. Review [Facebook for Developers](https://developers.facebook.com/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Crafting! 🎨✨**
