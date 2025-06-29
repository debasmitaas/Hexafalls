# Connecting Flutter Frontend to Backend

This guide will help you properly connect your Flutter frontend to the FastAPI backend.

## 1. Finding Your Computer's IP Address

### On Windows:
1. Open Command Prompt
2. Type `ipconfig` and press Enter
3. Look for `IPv4 Address` under your active network adapter (usually Wi-Fi or Ethernet)
4. Note the IP address (looks like `192.168.x.x`)

### On macOS:
1. Go to System Preferences > Network
2. Select your active connection (Wi-Fi or Ethernet)
3. The IP address appears on the right

## 2. Update Backend URL in Flutter App

Open `lib/main.dart` and update the `backendUrl` constant:

```dart
static const String backendUrl = 'http://YOUR_IP_ADDRESS:8000';
```

Replace `YOUR_IP_ADDRESS` with the IP address you found in step 1.

## 3. Ensure Backend Server is Running

1. Open a terminal/command prompt
2. Navigate to your backend folder:
   ```
   cd "f:\flutter app project\craftsmen-marketplace-backend"
   ```
3. Start the backend server:
   ```
   python main.py
   ```
4. Verify it's running by checking for the message: "Application startup complete"

## 4. Testing the Connection

1. Make sure your device is on the same Wi-Fi network as your computer
2. Run the Flutter app:
   ```
   flutter run
   ```
3. Try uploading a product with image and text
4. Watch the backend terminal for incoming requests

## Troubleshooting

### "Connection Refused" Error
- Ensure backend server is running
- Check IP address is correct
- Verify both devices are on the same network
- Check if your firewall is blocking connections

### "Network Error" in App
- Verify URL format (should be `http://192.168.x.x:8000`)
- Try opening the URL in a browser to see if the backend responds
- Check internet permissions in Android manifest

### Handling Image Upload Issues
- Check multipart/form-data is properly formatted
- Verify the upload endpoint is working with a tool like Postman
- Check if there are any size limits on image uploads

## Advanced: Different Environment URLs

For more sophisticated setup, you can detect the environment:

```dart
// Platform detection
import 'dart:io';

String getBackendUrl() {
  if (Platform.isAndroid) {
    // Check if running on emulator (this is simplified)
    return 'http://10.0.2.2:8000';
  } else if (Platform.isIOS) {
    // iOS simulator uses localhost
    return 'http://localhost:8000';
  } else {
    // Physical device or other platforms
    return 'http://192.168.133.28:8000';
  }
}
```
