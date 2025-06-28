# Speech Input Troubleshooting Guide

If the speech input is not working, follow these steps:

## 1. Check Permissions

### Android:
- Open your device Settings > Apps > Frontend (or your app name)
- Go to Permissions
- Ensure "Microphone" permission is granted
- If not granted, toggle it ON

### iOS:
- Open Settings > Privacy & Security > Microphone
- Find your app in the list and ensure it's toggled ON

## 2. Test Microphone Permission in App

1. Open the app
2. Look at the "Speech Debug Info" section at the bottom
3. Tap "Test Microphone Permission" button
4. Grant permission when prompted
5. Check if "Speech Available" shows "Yes"

## 3. Test Speech Recognition

1. Tap the microphone button next to "Product Name" field
2. You should see "Listening... Speak now!" in red text
3. Speak clearly into your device's microphone
4. Watch the debug info to see the status changes

## 4. Common Issues and Solutions

### "Speech recognition not available"
- **Solution**: Your device doesn't support speech recognition
- **Alternative**: Use manual text input

### "Microphone permission is required"
- **Solution**: Go to device Settings and grant microphone permission
- **Then**: Restart the app

### "Speech recognition error"
- **Solution**: Check your internet connection (some devices require internet for speech recognition)
- **Alternative**: Try again in a quieter environment

### Speech cuts off too early
- **Solution**: The app listens for 10 seconds. Speak within this time
- **Note**: There's a 3-second pause detection - avoid long pauses

### Can't hear any feedback
- **Solution**: The app doesn't provide audio feedback, only visual text updates
- **Check**: Look for text changes in the input fields and status messages

## 5. Device-Specific Issues

### Android Emulator:
- Speech recognition may not work properly in emulator
- **Solution**: Test on a physical Android device

### iOS Simulator:
- Microphone is not available in iOS Simulator
- **Solution**: Test on a physical iOS device

### Older Devices:
- Some older Android devices may not support speech-to-text
- **Solution**: Use manual text input as alternative

## 6. Network Issues

Some devices require internet connection for speech recognition:
- Ensure you have a stable internet connection
- Try both WiFi and mobile data

## 7. Testing Steps

1. **Basic Test**: 
   - Say "Hello world" into the microphone
   - Should appear in the text field

2. **Product Name Test**: 
   - Say "Handmade wooden table"
   - Should appear in Product Name field

3. **Price Test**: 
   - Say "Fifty dollars" or "50"
   - Should appear in Price field

## 8. Alternative Input Methods

If speech input doesn't work:
- Use the keyboard to type directly in the text fields
- All functionality will work the same way
- Speech is optional - manual input works perfectly

## 9. Debug Information

Check the debug panel at bottom of app:
- **Speech Available**: Should be "Yes"
- **Currently Listening**: Shows "Yes" when microphone button is pressed
- **Status**: Shows current speech recognition status

## 10. Getting Help

If issues persist:
1. Check the debug info in the app
2. Note your device model and OS version
3. Try on a different device if available
4. Use manual input as backup
