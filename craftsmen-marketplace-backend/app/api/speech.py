from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import base64

from app.core.database import get_db
from app.schemas.schemas import SpeechToTextRequest, SpeechToTextResponse
from app.services.speech_service import SpeechToTextService

router = APIRouter(prefix="/speech", tags=["speech"])

speech_service = SpeechToTextService()


@router.post("/text-to-speech", response_model=SpeechToTextResponse)
async def convert_speech_to_text(
    request: SpeechToTextRequest,
    db: Session = Depends(get_db)
):
    """Convert base64 encoded audio data to text"""
    
    try:
        result = await speech_service.convert_speech_to_text(
            audio_data=request.audio_data,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing speech: {str(e)}"
        )


@router.post("/audio-file-to-text", response_model=SpeechToTextResponse)
async def convert_audio_file_to_text(
    audio_file: UploadFile = File(...),
    language: str = "en-US",
    db: Session = Depends(get_db)
):
    """Convert uploaded audio file to text"""
    
    # Validate file type
    allowed_audio_types = [".wav", ".mp3", ".m4a", ".flac", ".webm"]
    if not any(audio_file.filename.lower().endswith(ext) for ext in allowed_audio_types):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio file type. Allowed types: {', '.join(allowed_audio_types)}"
        )
    
    try:
        # Save uploaded file temporarily
        temp_file_path = f"temp_{audio_file.filename}"
        contents = await audio_file.read()
        
        with open(temp_file_path, "wb") as f:
            f.write(contents)
        
        # Convert to text
        result = await speech_service.convert_audio_file_to_text(
            file_path=temp_file_path,
            language=language
        )
        
        # Clean up temp file
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        return result
        
    except Exception as e:
        # Clean up temp file on error
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio file: {str(e)}"
        )
