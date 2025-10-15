"""
Transcription Service for Meeting Summarizer application.

This module provides audio transcription capabilities using OpenAI's Whisper API.
It handles audio file validation, transcription with standard and verbose formats,
and comprehensive error handling.

Created on: October 13, 2025
"""

from openai import OpenAI
import os
from django.conf import settings
import logging
from typing import Tuple, Dict, Optional, Any

# Set up logging
logger = logging.getLogger(__name__)


class TranscriptionService:
    """
    Service class for transcribing audio files using OpenAI Whisper API.
    
    This service provides methods for:
    - Audio file validation
    - Standard transcription
    - Transcription with timestamps
    
    Attributes:
        api_key (str): OpenAI API key
        client (OpenAI): OpenAI client instance
        model (str): Whisper model name ('whisper-1')
    
    Example:
        >>> service = TranscriptionService()
        >>> transcript = service.transcribe_audio('/path/to/audio.mp3')
        >>> print(transcript)
    """
    
    # Whisper API file size limit (25 MB)
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
    
    # Supported audio file extensions
    SUPPORTED_FORMATS = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize transcription service with OpenAI client.
        
        Args:
            base_url (str, optional): Custom API base URL. If not provided,
                                     will use Groq (free) or OpenAI from settings.
        
        Raises:
            ValueError: If API key is not configured
        """
        from django.conf import settings
        
        # Check if Groq API key is available (FREE option)
        groq_api_key = getattr(settings, 'GROQ_API_KEY', '')
        
        if groq_api_key:
            # Use FREE Groq API for Whisper transcription
            self.api_key = groq_api_key
            self.base_url = getattr(settings, 'GROQ_BASE_URL', 'https://api.groq.com/openai/v1')
            self.model = getattr(settings, 'GROQ_WHISPER_MODEL', 'whisper-large-v3')
            logger.info(f"TranscriptionService initialized with FREE Groq API: {self.base_url}")
            logger.info(f"Using Groq Whisper model: {self.model}")
        else:
            # Fallback to OpenAI-compatible API (OpenRouter/Llama Maverick)
            self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
            self.base_url = base_url or getattr(settings, 'OPENAI_BASE_URL', None)
            self.model = getattr(settings, 'OPENAI_WHISPER_MODEL', 'whisper-1')
            
            if self.base_url:
                logger.info(f"TranscriptionService initialized with custom base_url: {self.base_url}")
            
        if not self.api_key:
            raise ValueError("API key not configured. Set GROQ_API_KEY or OPENAI_API_KEY in settings.")
        
        # Initialize OpenAI client with custom base URL
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        self.timeout = getattr(settings, 'OPENAI_TIMEOUT', 300)
        self.max_retries = getattr(settings, 'OPENAI_MAX_RETRIES', 3)
        
        logger.info("TranscriptionService initialized successfully")
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate audio file exists and is within size limits.
        
        Performs the following checks:
        1. File exists at the given path
        2. File size is within Whisper API limit (25 MB)
        3. File extension is supported
        
        Args:
            file_path (str): Path to the audio file to validate
        
        Returns:
            tuple: (is_valid, error_message)
                - is_valid (bool): True if file is valid, False otherwise
                - error_message (str or None): Error description if invalid, None if valid
        
        Example:
            >>> service = TranscriptionService()
            >>> is_valid, error = service.validate_audio_file('/path/to/audio.mp3')
            >>> if not is_valid:
            ...     print(f"Validation failed: {error}")
        """
        # Check if file exists
        if not os.path.exists(file_path):
            error_msg = f"Audio file not found: {file_path}"
            logger.error(error_msg)
            return False, error_msg
        
        # Check if it's a file (not a directory)
        if not os.path.isfile(file_path):
            error_msg = f"Path is not a file: {file_path}"
            logger.error(error_msg)
            return False, error_msg
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE:
            file_size_mb = file_size / (1024 * 1024)
            max_size_mb = self.MAX_FILE_SIZE / (1024 * 1024)
            error_msg = (
                f"File size ({file_size_mb:.2f} MB) exceeds Whisper API limit "
                f"({max_size_mb} MB)"
            )
            logger.error(error_msg)
            return False, error_msg
        
        # Check file extension
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        
        if file_extension not in self.SUPPORTED_FORMATS:
            error_msg = (
                f"Unsupported file format: {file_extension}. "
                f"Supported formats: {', '.join(sorted(self.SUPPORTED_FORMATS))}"
            )
            logger.error(error_msg)
            return False, error_msg
        
        # File is valid
        logger.info(f"Audio file validated successfully: {file_path}")
        return True, None
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using OpenAI Whisper API.
        
        This method validates the audio file, sends it to the Whisper API,
        and returns the transcribed text.
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe
        
        Returns:
            str: Transcribed text from the audio file
        
        Raises:
            ValueError: If audio file validation fails
            Exception: If API call fails or other errors occur
        
        Example:
            >>> service = TranscriptionService()
            >>> transcript = service.transcribe_audio('/path/to/meeting.mp3')
            >>> print(f"Transcript: {transcript}")
        """
        logger.info(f"Starting transcription for: {audio_file_path}")
        
        try:
            # Validate audio file first
            is_valid, error_message = self.validate_audio_file(audio_file_path)
            if not is_valid:
                raise ValueError(f"Audio file validation failed: {error_message}")
            
            # Open and transcribe the audio file
            with open(audio_file_path, 'rb') as audio_file:
                logger.info(f"Sending file to Whisper API: {os.path.basename(audio_file_path)}")
                
                # Call Whisper API
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format='text'
                )
                
                # Log success
                transcript_length = len(transcript) if transcript else 0
                logger.info(
                    f"Transcription completed successfully. "
                    f"Transcript length: {transcript_length} characters"
                )
                
                return transcript
        
        except ValueError as ve:
            # Re-raise validation errors
            logger.error(f"Validation error: {str(ve)}")
            raise
        
        except FileNotFoundError as fnf:
            error_msg = f"Audio file not found: {audio_file_path}"
            logger.error(error_msg)
            raise Exception(error_msg) from fnf
        
        except Exception as e:
            error_msg = f"Transcription failed for {audio_file_path}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg) from e
    
    def transcribe_with_timestamps(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio with word-level timestamps and detailed metadata.
        
        This method provides verbose transcription output including:
        - Full transcript text
        - Word-level timestamps
        - Segment information
        - Language detection
        - Duration
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe
        
        Returns:
            dict: Structured transcription data with the following keys:
                - text (str): Full transcript text
                - language (str): Detected language code
                - duration (float): Audio duration in seconds
                - segments (list): List of segments with timestamps
                - words (list): List of words with timestamps (if available)
        
        Raises:
            ValueError: If audio file validation fails
            Exception: If API call fails or other errors occur
        
        Example:
            >>> service = TranscriptionService()
            >>> result = service.transcribe_with_timestamps('/path/to/meeting.mp3')
            >>> print(f"Language: {result['language']}")
            >>> print(f"Duration: {result['duration']} seconds")
            >>> for segment in result['segments']:
            ...     print(f"[{segment['start']:.2f}s] {segment['text']}")
        """
        logger.info(f"Starting transcription with timestamps for: {audio_file_path}")
        
        try:
            # Validate audio file first
            is_valid, error_message = self.validate_audio_file(audio_file_path)
            if not is_valid:
                raise ValueError(f"Audio file validation failed: {error_message}")
            
            # Open and transcribe the audio file with verbose output
            with open(audio_file_path, 'rb') as audio_file:
                logger.info(
                    f"Sending file to Whisper API (verbose mode): "
                    f"{os.path.basename(audio_file_path)}"
                )
                
                # Call Whisper API with verbose JSON response
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format='verbose_json',
                    timestamp_granularities=['word', 'segment']
                )
                
                # Parse and structure the response
                result = {
                    'text': response.text,
                    'language': getattr(response, 'language', 'unknown'),
                    'duration': getattr(response, 'duration', 0.0),
                    'segments': [],
                    'words': []
                }
                
                # Extract segments if available
                if hasattr(response, 'segments') and response.segments:
                    result['segments'] = [
                        {
                            'id': getattr(seg, 'id', idx),
                            'start': getattr(seg, 'start', 0.0),
                            'end': getattr(seg, 'end', 0.0),
                            'text': getattr(seg, 'text', ''),
                        }
                        for idx, seg in enumerate(response.segments)
                    ]
                
                # Extract words if available
                if hasattr(response, 'words') and response.words:
                    result['words'] = [
                        {
                            'word': getattr(word, 'word', ''),
                            'start': getattr(word, 'start', 0.0),
                            'end': getattr(word, 'end', 0.0),
                        }
                        for word in response.words
                    ]
                
                # Log success
                logger.info(
                    f"Transcription with timestamps completed. "
                    f"Language: {result['language']}, "
                    f"Duration: {result['duration']:.2f}s, "
                    f"Segments: {len(result['segments'])}, "
                    f"Words: {len(result['words'])}"
                )
                
                return result
        
        except ValueError as ve:
            # Re-raise validation errors
            logger.error(f"Validation error: {str(ve)}")
            raise
        
        except FileNotFoundError as fnf:
            error_msg = f"Audio file not found: {audio_file_path}"
            logger.error(error_msg)
            raise Exception(error_msg) from fnf
        
        except Exception as e:
            error_msg = (
                f"Transcription with timestamps failed for {audio_file_path}: {str(e)}"
            )
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg) from e
    
    def get_audio_duration(self, audio_file_path: str) -> Optional[int]:
        """
        Get audio file duration in seconds using mutagen library.
        
        Args:
            audio_file_path (str): Path to the audio file
        
        Returns:
            int: Duration in seconds, or None if unable to determine
        """
        try:
            from mutagen import File
            audio = File(audio_file_path)
            if audio and audio.info:
                duration = int(audio.info.length)
                logger.info(f"Audio duration: {duration} seconds")
                return duration
        except Exception as e:
            logger.warning(f"Could not determine audio duration: {str(e)}")
        return None
