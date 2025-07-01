import os
import sys
from pathlib import Path
from mangum import Mangum

# Add the project root to Python path for proper module resolution
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Now import the main app
try:
    from main import app
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback: try to import with explicit path manipulation
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / "app"))
    from main import app

# Add Mangum handler for serverless deployment
handler = Mangum(app)
