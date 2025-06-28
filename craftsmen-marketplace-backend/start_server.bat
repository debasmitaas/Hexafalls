@echo off
echo Starting Craftsmen Marketplace Backend...
echo.
echo 🚀 Server will be available at:
echo    - API: http://localhost:8000
echo    - Docs: http://localhost:8000/docs
echo    - ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

uv run python main.py
