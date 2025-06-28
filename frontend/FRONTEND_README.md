# Craftsmen Marketplace Flutter Frontend

A Flutter mobile app for craftsmen to upload product images, use native speech-to-text for product details, and automatically post to Facebook and Instagram.

## Features

- **Image Upload**: Select product images from gallery
- **Native Speech-to-Text**: Use voice input for product name and price
- **Social Media Integration**: Automatically post to Facebook and Instagram
- **AI Caption Generation**: AI-generated captions for social media posts
- **Real-time Feedback**: Success/error notifications

## Setup Instructions

### Prerequisites

1. **Flutter SDK**: Install Flutter following the [official guide](https://docs.flutter.dev/get-started/install)
2. **Backend Server**: Ensure the FastAPI backend is running at `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd "f:\flutter app project\frontend"
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. For Android development, ensure you have:
   - Android Studio installed
   - Android SDK configured
   - An Android emulator running or physical device connected

### Running the App

1. Start the backend server first:
   ```bash
   cd "f:\flutter app project\craftsmen-marketplace-backend"
   python main.py
   ```

2. Run the Flutter app:
   ```bash
   cd "f:\flutter app project\frontend"
   flutter run
   ```

### Permissions

The app requires the following permissions:
- **Microphone**: For speech-to-text functionality
- **Camera/Storage**: For image selection
- **Internet**: For API communication

These permissions are automatically requested when needed.

## Usage

1. **Select Image**: Tap "Select Image" to choose a product photo from your gallery
2. **Enter Product Name**: Type or use the microphone button for speech input
3. **Enter Price**: Type or use the microphone button for speech input
4. **Post to Social Media**: Tap "Post to Instagram & Facebook" to upload and post

## Backend Integration

The app connects to the FastAPI backend at `http://localhost:8000` and uses the following endpoint:
- `POST /native_products/create-and-post-native`: Upload product and post to social media

## Troubleshooting

### Common Issues

1. **Backend Connection Error**: 
   - Ensure the backend server is running on port 8000
   - Check that your device/emulator can access localhost

2. **Speech Recognition Not Working**:
   - Grant microphone permissions when prompted
   - Ensure you're in a quiet environment
   - Check device microphone functionality

3. **Image Upload Issues**:
   - Grant storage/camera permissions when prompted
   - Ensure the selected image is accessible

### For Physical Device Testing

If testing on a physical device, you may need to:
1. Replace `localhost` with your computer's IP address in `main.dart`
2. Ensure both devices are on the same network
3. Configure backend to accept connections from other hosts

## Configuration

To change the backend URL, edit the `backendUrl` constant in `lib/main.dart`:

```dart
static const String backendUrl = 'http://YOUR_BACKEND_URL:8000';
```

## Dependencies

- `image_picker`: Image selection from gallery
- `speech_to_text`: Native speech recognition
- `permission_handler`: Runtime permission management
- `http`: HTTP requests to backend
- `flutter/material`: UI components
