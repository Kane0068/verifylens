from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os
from ..core.analyzer import MediaAnalyzer
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="VerifyLens API",
    description="AI-powered media verification platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize analyzer
analyzer = MediaAnalyzer(os.getenv("GEMINI_API_KEY"))

@app.get("/")
async def root():
    """
    Root endpoint that provides API information.
    """
    return {
        "name": "VerifyLens API",
        "version": "1.0.0",
        "description": "AI-powered media verification platform",
        "endpoints": {
            "/analyze/{media_type}": "POST - Analyze media file",
            "/usage": "GET - Get token usage statistics",
            "/docs": "GET - API documentation"
        }
    }


@app.post("/analyze/{media_type}")
async def analyze_media(
    media_type: str,
    file: UploadFile = File(...),
    #token: str = Depends(oauth2_scheme)
) -> Dict[str, Any]:
    """
    Analyze uploaded media file.
    """
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Perform analysis
        result = analyzer.analyze_media(temp_path, media_type)
        
        # Clean up
        os.remove(temp_path)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usage")
async def get_usage(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get token usage statistics.
    """
    return analyzer.get_usage_stats()
