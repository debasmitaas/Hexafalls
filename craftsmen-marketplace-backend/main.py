import sys
import os
from pathlib import Path

# Add the project root to Python path for proper module resolution
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

# Print debug info for cloud deployment troubleshooting
print(f"Python path: {sys.path[:3]}")
print(f"Project root: {project_root}")
print(f"Current working directory: {os.getcwd()}")

try:
    from fastapi import FastAPI, Depends
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    print("✓ FastAPI imports successful")
except ImportError as e:
    print(f"✗ FastAPI import error: {e}")
    raise

try:
    from app.core.config import settings
    from app.core.database import engine, Base
    print("✓ Core module imports successful")
except ImportError as e:
    print(f"✗ Core module import error: {e}")
    print(f"Available files in app/core: {list((project_root / 'app' / 'core').glob('*.py'))}")
    raise

try:
    from app.api import products, orders, speech, automation, native_products, native_speech, ai, native_products_compat
    print("✓ API module imports successful")
    api_modules_loaded = True
except ImportError as e:
    print(f"✗ API module import error: {e}")
    # Set flag to skip router inclusion
    api_modules_loaded = False

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Backend API for Craftsmen Marketplace - helping craftsmen showcase and sell their work",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers only if modules loaded successfully
if api_modules_loaded:
    app.include_router(products.router, prefix="/api")
    app.include_router(orders.router, prefix="/api")
    app.include_router(speech.router, prefix="/api")
    app.include_router(automation.router, prefix="/api")
    app.include_router(native_products.router, prefix="/api")
    app.include_router(native_speech.router, prefix="/api")
    app.include_router(ai.router, prefix="/ai", tags=["AI"])
    app.include_router(native_products_compat.router)  # Direct path for frontend compatibility
else:
    print("⚠️ Skipping API router inclusion due to import errors")

# Create uploads directory
os.makedirs(settings.upload_folder, exist_ok=True)

# Serve uploaded files
app.mount(f"/{settings.upload_folder}", StaticFiles(directory=settings.upload_folder), name="uploads")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Craftsmen Marketplace API",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
