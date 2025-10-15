"""
Django forms for Meeting Summarizer application.

This module contains form definitions for:
- Meeting upload with audio file validation

Created on: October 13, 2025
"""

# ============================================
# 1. IMPORT REQUIRED MODULES
# ============================================
from django import forms
from django.core.exceptions import ValidationError
from .models import Meeting
import os


# ============================================
# 2. MEETING UPLOAD FORM CLASS (MODELFORM)
# ============================================

class MeetingUploadForm(forms.ModelForm):
    """
    ModelForm for uploading meeting audio files.
    
    Features:
    - Audio file upload with comprehensive validation
    - Optional title field with automatic fallback to filename
    - File size validation (max 100MB)
    - File extension validation (.mp3, .wav, .m4a)
    - Bootstrap styling
    - Helpful error messages
    """
    
    class Meta:
        model = Meeting
        fields = ['audio_file', 'title']
        
        # Custom widgets with Bootstrap classes and attributes
        widgets = {
            'audio_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.mp3,.wav,.m4a',
                'id': 'audioFileInput'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter meeting title'
            }),
        }
        
        # Help text for each field
        help_texts = {
            'audio_file': 'Upload an audio file (MP3, WAV, or M4A). Maximum size: 100MB.',
            'title': 'Enter a title for the meeting. If left blank, the filename will be used.',
        }
    
    def clean_audio_file(self):
        """
        Validate uploaded audio file.
        
        Performs the following validations:
        - Checks file extension (only .mp3, .wav, .m4a allowed)
        - Checks file size (maximum 100MB)
        
        Returns:
            File: Validated audio file object
            
        Raises:
            ValidationError: If file extension or size is invalid
        """
        audio_file = self.cleaned_data.get('audio_file')
        
        if audio_file:
            # Get file extension
            file_name = audio_file.name.lower()
            file_extension = os.path.splitext(file_name)[1]
            
            # Check file extension (.mp3, .wav, .m4a only)
            allowed_extensions = ['.mp3', '.wav', '.m4a']
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f'Invalid file type "{file_extension}". '
                    f'Only {", ".join(allowed_extensions)} files are allowed.'
                )
            
            # Check file size (max 100MB)
            max_size = 100 * 1024 * 1024  # 100MB in bytes
            if audio_file.size > max_size:
                actual_size_mb = audio_file.size / (1024 * 1024)
                raise ValidationError(
                    f'File size ({actual_size_mb:.2f}MB) exceeds the maximum allowed size of 100MB. '
                    f'Please upload a smaller file.'
                )
        
        return audio_file
    
    def clean_title(self):
        """
        Clean and validate the title field.
        
        - Strips leading/trailing whitespace
        - If empty after stripping, uses the audio filename as title
        
        Returns:
            str: Cleaned title string
        """
        title = self.cleaned_data.get('title', '').strip()
        
        # If title is empty, use audio filename (without extension)
        if not title:
            audio_file = self.cleaned_data.get('audio_file')
            if audio_file:
                # Extract filename without extension
                filename = os.path.splitext(audio_file.name)[0]
                title = filename
        
        return title
