"""
Django models for Meeting Summarizer application.

This module defines the core data models for storing and managing:
- Meeting recordings and metadata
- Transcripts generated from audio
- AI-generated summaries
- Action items extracted from meetings

Created on: October 13, 2025
"""

# ============================================
# 1. IMPORT REQUIRED MODULES
# ============================================
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os
import json


# ============================================
# 2. MEETING MODEL
# ============================================

class Meeting(models.Model):
    """
    Represents a meeting with audio recording and processing status.
    
    This model stores the uploaded audio file and tracks the processing
    status through various stages: pending → processing → completed/failed.
    
    Attributes:
        audio_file (FileField): Uploaded audio file (MP3, WAV, M4A, etc.)
        title (CharField): Meeting title/name
        duration (IntegerField): Audio duration in seconds
        status (CharField): Processing status (pending/processing/completed/failed)
        created_at (DateTimeField): Timestamp when meeting was created
        updated_at (DateTimeField): Timestamp when meeting was last updated
        file_size (IntegerField): Audio file size in bytes
    """
    
    # Status choices for meeting processing workflow
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Audio file field with upload path and validation
    audio_file = models.FileField(
        upload_to='meetings/audio/',
        max_length=500,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp3', 'wav', 'm4a', 'ogg', 'flac']
            )
        ],
        help_text='Upload audio file (MP3, WAV, M4A, OGG, or FLAC format)'
    )
    
    # Meeting metadata
    title = models.CharField(
        max_length=200,
        default='Untitled Meeting',
        help_text='Meeting title or name'
    )
    
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text='Duration in seconds'
    )
    
    # Processing status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,  # Index for faster status queries
        help_text='Current processing status'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when meeting was created'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when meeting was last updated'
    )
    
    # File information
    file_size = models.IntegerField(
        null=True,
        blank=True,
        help_text='File size in bytes'
    )
    
    # Additional fields (optional but useful)
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Optional notes or description'
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text='Error message if processing failed'
    )
    
    is_starred = models.BooleanField(
        default=False,
        help_text='Whether this meeting is starred/favorited'
    )
    
    class Meta:
        """Model metadata configuration."""
        ordering = ['-created_at']  # Show newest meetings first
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        """String representation of the meeting."""
        return self.title
    
    def get_duration_display(self):
        """
        Return formatted duration in MM:SS format.
        
        Returns:
            str: Duration formatted as "MM:SS" (e.g., "5:30")
                 or "N/A" if duration is not set
        
        Examples:
            >>> meeting.duration = 330  # 5 minutes 30 seconds
            >>> meeting.get_duration_display()
            '5:30'
        """
        if self.duration is None:
            return "N/A"
        
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    
    def get_file_size_display(self):
        """
        Return formatted file size in MB or KB.
        
        Returns:
            str: File size formatted as "X.XX MB" or "XXX KB"
                 or "N/A" if file_size is not set
        
        Examples:
            >>> meeting.file_size = 2500000  # 2.5 MB
            >>> meeting.get_file_size_display()
            '2.38 MB'
        """
        if self.file_size is None:
            return "N/A"
        
        # Convert to MB if size is large enough
        if self.file_size >= 1024 * 1024:  # 1 MB or more
            size_mb = self.file_size / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        else:
            size_kb = self.file_size / 1024
            return f"{size_kb:.1f} KB"
    
    def get_absolute_url(self):
        """
        Return the absolute URL for this meeting's detail page.
        
        Returns:
            str: URL path to meeting detail view
        """
        from django.urls import reverse
        return reverse('meeting_detail', kwargs={'pk': self.pk})
    
    def delete(self, *args, **kwargs):
        """
        Override delete to remove audio file from storage.
        
        This ensures that when a meeting is deleted, the associated
        audio file is also removed from the file system.
        """
        # Delete the audio file from storage
        if self.audio_file:
            if os.path.isfile(self.audio_file.path):
                os.remove(self.audio_file.path)
        
        # Call parent delete method
        super().delete(*args, **kwargs)
    
    @property
    def is_completed(self):
        """Check if meeting processing is completed."""
        return self.status == 'completed'
    
    @property
    def is_failed(self):
        """Check if meeting processing has failed."""
        return self.status == 'failed'
    
    @property
    def is_processing(self):
        """Check if meeting is currently being processed."""
        return self.status == 'processing'


# ============================================
# 3. TRANSCRIPT MODEL
# ============================================

class Transcript(models.Model):
    """
    Stores the transcript text generated from meeting audio.
    
    This model contains the full text transcription of the meeting
    audio, generated using OpenAI Whisper or similar ASR service.
    
    Attributes:
        meeting (ForeignKey): Related meeting record
        text (TextField): Full transcript text
        language (CharField): Detected language code (e.g., 'en')
        word_count (IntegerField): Number of words in transcript
        created_at (DateTimeField): Timestamp when transcript was created
    """
    
    # Foreign key to Meeting with cascade delete
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='transcripts',
        help_text='Related meeting record'
    )
    
    # Transcript content
    text = models.TextField(
        help_text='Full transcript text'
    )
    
    # Language information
    language = models.CharField(
        max_length=10,
        default='en',
        help_text='Language code (e.g., en, es, fr)'
    )
    
    # Metadata
    word_count = models.IntegerField(
        default=0,
        help_text='Number of words in transcript'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when transcript was created'
    )
    
    # Optional: confidence score from ASR
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        help_text='ASR confidence score (0.0 to 1.0)'
    )
    
    class Meta:
        """Model metadata configuration."""
        verbose_name = 'Transcript'
        verbose_name_plural = 'Transcripts'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the transcript."""
        return f'Transcript for {self.meeting.title}'
    
    def save(self, *args, **kwargs):
        """
        Override save to automatically calculate word count.
        
        This method counts the words in the transcript text
        before saving the record to the database.
        """
        # Calculate word count if text is provided
        if self.text:
            # Split by whitespace and count non-empty words
            words = self.text.split()
            self.word_count = len(words)
        else:
            self.word_count = 0
        
        # Call parent save method
        super().save(*args, **kwargs)
    
    def get_excerpt(self, max_words=50):
        """
        Return an excerpt of the transcript.
        
        Args:
            max_words (int): Maximum number of words to include
        
        Returns:
            str: Excerpt of transcript text
        """
        if not self.text:
            return ""
        
        words = self.text.split()
        if len(words) <= max_words:
            return self.text
        
        excerpt = ' '.join(words[:max_words])
        return f"{excerpt}..."
    
    @property
    def character_count(self):
        """Return the number of characters in the transcript."""
        return len(self.text) if self.text else 0


# ============================================
# 4. SUMMARY MODEL
# ============================================

class Summary(models.Model):
    """
    Stores AI-generated summary of the meeting.
    
    This model contains the executive summary and structured data
    extracted from the meeting, including key decisions and topics.
    
    Attributes:
        meeting (OneToOneField): Related meeting record (one-to-one)
        executive_summary (TextField): Brief overview of meeting
        key_decisions (JSONField): List of key decisions made
        discussion_topics (JSONField): Main topics discussed
        created_at (DateTimeField): Timestamp when summary was created
    """
    
    # One-to-one relationship with Meeting
    meeting = models.OneToOneField(
        Meeting,
        on_delete=models.CASCADE,
        related_name='summary',
        help_text='Related meeting record'
    )
    
    # Summary content
    executive_summary = models.TextField(
        help_text='Brief overview of meeting'
    )
    
    # Structured data stored as JSON
    key_decisions = models.JSONField(
        default=list,
        help_text='List of key decisions made during the meeting'
    )
    
    discussion_topics = models.JSONField(
        default=list,
        help_text='Main topics discussed during the meeting'
    )
    
    # Additional structured fields (optional)
    participants = models.JSONField(
        default=list,
        blank=True,
        help_text='List of meeting participants (if detected)'
    )
    
    insights = models.JSONField(
        default=list,
        blank=True,
        help_text='Key insights or takeaways'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when summary was created'
    )
    
    class Meta:
        """Model metadata configuration."""
        verbose_name = 'Summary'
        verbose_name_plural = 'Summaries'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the summary."""
        return f'Summary for {self.meeting.title}'
    
    def get_decision_count(self):
        """Return the number of key decisions."""
        return len(self.key_decisions) if isinstance(self.key_decisions, list) else 0
    
    def get_topic_count(self):
        """Return the number of discussion topics."""
        return len(self.discussion_topics) if isinstance(self.discussion_topics, list) else 0
    
    def get_summary_excerpt(self, max_chars=200):
        """
        Return an excerpt of the executive summary.
        
        Args:
            max_chars (int): Maximum number of characters to include
        
        Returns:
            str: Excerpt of executive summary
        """
        if not self.executive_summary:
            return ""
        
        if len(self.executive_summary) <= max_chars:
            return self.executive_summary
        
        return f"{self.executive_summary[:max_chars]}..."


# ============================================
# 5. ACTION ITEM MODEL
# ============================================

class ActionItem(models.Model):
    """
    Represents an action item or task extracted from the meeting.
    
    This model stores tasks, assignments, and deadlines identified
    during the meeting discussion.
    
    Attributes:
        meeting (ForeignKey): Related meeting record
        task (CharField): Task description
        assignee (CharField): Person assigned to the task
        deadline (DateField): Task deadline
        priority (CharField): Task priority (high/medium/low)
        is_completed (BooleanField): Whether task is completed
        created_at (DateTimeField): Timestamp when action item was created
    """
    
    # Priority choices
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    # Foreign key to Meeting with cascade delete
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='action_items',
        help_text='Related meeting record'
    )
    
    # Task information
    title = models.CharField(
        max_length=300,
        default='Untitled Task',
        help_text='Task title (auto-populated from task description)'
    )
    
    task = models.CharField(
        max_length=300,
        help_text='Task or action item description'
    )
    
    assignee = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Person assigned to this task'
    )
    
    deadline = models.DateField(
        null=True,
        blank=True,
        help_text='Task deadline date'
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        db_index=True,  # Index for faster priority queries
        help_text='Task priority level'
    )
    
    # Status tracking
    is_completed = models.BooleanField(
        default=False,
        help_text='Whether the task has been completed'
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when task was marked as completed'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when action item was created'
    )
    
    # Optional fields
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Additional notes or context for this task'
    )
    
    class Meta:
        """Model metadata configuration."""
        ordering = ['-priority', 'deadline', '-created_at']  # High priority first, then by deadline
        verbose_name = 'Action Item'
        verbose_name_plural = 'Action Items'
        indexes = [
            models.Index(fields=['priority', 'deadline']),
            models.Index(fields=['is_completed']),
        ]
    
    def __str__(self):
        """String representation of the action item."""
        return self.task[:50]  # Return first 50 characters
    
    def mark_completed(self):
        """
        Mark this action item as completed.
        
        Sets is_completed to True and records the completion timestamp.
        """
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        """
        Mark this action item as incomplete.
        
        Sets is_completed to False and clears the completion timestamp.
        """
        self.is_completed = False
        self.completed_at = None
        self.save()
    
    @property
    def is_overdue(self):
        """
        Check if the action item is overdue.
        
        Returns:
            bool: True if deadline has passed and task is not completed
        """
        if self.deadline and not self.is_completed:
            return self.deadline < timezone.now().date()
        return False
    
    @property
    def days_until_deadline(self):
        """
        Calculate days until deadline.
        
        Returns:
            int: Number of days until deadline (negative if overdue)
            None: If no deadline is set
        """
        if self.deadline:
            delta = self.deadline - timezone.now().date()
            return delta.days
        return None
    
    def get_status_display_with_icon(self):
        """
        Return status with appropriate icon/emoji.
        
        Returns:
            str: Status with icon (e.g., "✅ Completed", "⏳ Pending")
        """
        if self.is_completed:
            return "✅ Completed"
        elif self.is_overdue:
            return "🔴 Overdue"
        elif self.days_until_deadline and self.days_until_deadline <= 3:
            return "⚠️ Due Soon"
        else:
            return "⏳ Pending"


# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_meeting_statistics():
    """
    Calculate overall meeting statistics.
    
    Returns:
        dict: Statistics including total meetings, completed, etc.
    """
    from django.db.models import Count, Sum, Avg
    
    stats = {
        'total_meetings': Meeting.objects.count(),
        'completed_meetings': Meeting.objects.filter(status='completed').count(),
        'pending_meetings': Meeting.objects.filter(status='pending').count(),
        'failed_meetings': Meeting.objects.filter(status='failed').count(),
        'total_action_items': ActionItem.objects.count(),
        'completed_action_items': ActionItem.objects.filter(is_completed=True).count(),
    }
    
    return stats
