#!/usr/bin/env python3
import requests
import os
from pathlib import Path

# Find an image file
uploads_dir = Path('uploads')
images = list(uploads_dir.glob('*.jpg')) + list(uploads_dir.glob('*.png')) + list(uploads_dir.glob('*.JPG'))

if images:
    image_path = images[0]
    print(f'Testing with image: {image_path}')
    
    # Test the EXACT same endpoint the frontend uses
    with open(image_path, 'rb') as f:
        files = {'image_file': f}
        data = {
            'name': 'Test Silver Ring',
            'price': 800,
            'description': 'Beautiful silver ring',
            'category': 'jewelry'
        }
        
        response = requests.post(
            'http://localhost:8000/native_products/create-and-post-native',
            files=files,
            data=data
        )
        
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            result = response.json()
            ai_caption = result.get('product', {}).get('ai_caption', 'NO CAPTION')
            print(f'AI Caption: {ai_caption}')
            print('---')
            print(f'Full response: {result}')
        else:
            print(f'Error: {response.text}')
else:
    print('No images found')
