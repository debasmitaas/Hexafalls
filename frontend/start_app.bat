@echo off
echo Starting Craftsmen Marketplace Frontend...
echo.

echo 1. Checking Flutter installation...
flutter --version
if %errorlevel% neq 0 (
    echo ERROR: Flutter is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo 2. Installing dependencies...
flutter pub get
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 3. Checking for connected devices...
flutter devices

echo.
echo 4. Starting the app...
echo Make sure your backend server is running at http://localhost:8000
echo.
pause
flutter run

pause
