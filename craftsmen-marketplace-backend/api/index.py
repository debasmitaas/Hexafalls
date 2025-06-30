from fastapi import FastAPI
import os
from mangum import Mangum
import sys

# Import your main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

# Add Mangum handler for AWS Lambda/Vercel
handler = Mangum(app)
