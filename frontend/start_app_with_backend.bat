@echo off
echo Starting Craftsmen Marketplace App...
echo.

echo === Finding your local IP address ===
ipconfig | findstr /i "IPv4"
echo.
echo Look for IPv4 Address that looks like "192.168.x.x"
echo You should use this IP in your Flutter app's backendUrl variable
echo.

echo === Starting Backend Server ===
echo Make sure you update your Flutter app with the correct IP address!
cd "..\craftsmen-marketplace-backend"
start cmd /k python main.py
echo.

echo === Starting Flutter Frontend ===
cd "..\frontend"
echo.
echo Running Flutter app...
flutter run

pause
