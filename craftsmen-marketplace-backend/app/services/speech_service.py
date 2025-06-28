import base64
import io
from app.core.config import settings
from app.schemas.schemas import SpeechToTextResponse

try:
    from google.cloud import speech
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False


class SpeechToTextService:
    """Service for converting speech to text using Google Cloud Speech-to-Text API"""
    
    def __init__(self):
        self.client = None
        if GOOGLE_CLOUD_AVAILABLE and settings.google_application_credentials:
            try:
                self.client = speech.SpeechClient()
            except Exception as e:
                print(f"Warning: Could not initialize Google Speech client: {str(e)}")
                self.client = None
    
    async def convert_speech_to_text(self, audio_data: str, language: str = "en-US") -> SpeechToTextResponse:
        """
        Convert base64 encoded audio data to text
        
        Args:
            audio_data: Base64 encoded audio data
            language: Language code (default: en-US)
            
        Returns:
            SpeechToTextResponse with text and confidence
        """
        if not self.client:
            return SpeechToTextResponse(
                text="Speech-to-text service not available. Please configure Google Cloud credentials.",
                confidence=0.0
            )
        
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Configure recognition
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code=language,
                enable_automatic_punctuation=True,
            )
            
            # Perform the transcription
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                # Get the first result with highest confidence
                result = response.results[0]
                alternative = result.alternatives[0]
                
                return SpeechToTextResponse(
                    text=alternative.transcript,
                    confidence=alternative.confidence
                )
            else:
                return SpeechToTextResponse(
                    text="",
                    confidence=0.0
                )
                
        except Exception as e:
            print(f"Error in speech-to-text conversion: {str(e)}")
            return SpeechToTextResponse(
                text="",
                confidence=0.0
            )
    
    async def convert_audio_file_to_text(self, file_path: str, language: str = "en-US") -> SpeechToTextResponse:
        """
        Convert audio file to text
        
        Args:
            file_path: Path to the audio file
            language: Language code (default: en-US)
            
        Returns:
            SpeechToTextResponse with text and confidence
        """
        if not self.client:
            return SpeechToTextResponse(
                text="Speech-to-text service not available. Please configure Google Cloud credentials.",
                confidence=0.0
            )
        
        try:
            with io.open(file_path, "rb") as audio_file:
                content = audio_file.read()
                
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language,
                enable_automatic_punctuation=True,
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                alternative = result.alternatives[0]
                
                return SpeechToTextResponse(
                    text=alternative.transcript,
                    confidence=alternative.confidence
                )
            else:
                return SpeechToTextResponse(
                    text="",
                    confidence=0.0
                )
                
        except Exception as e:
            print(f"Error in audio file conversion: {str(e)}")
            return SpeechToTextResponse(
                text="",
                confidence=0.0
            )
