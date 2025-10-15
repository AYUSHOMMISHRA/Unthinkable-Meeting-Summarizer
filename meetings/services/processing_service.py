"""
Processing Service for Meeting Summarizer application.

This module orchestrates the complete meeting processing workflow:
1. Audio transcription using Whisper API
2. AI summarization using GPT/Llama models
3. Action item extraction
4. Database persistence

Created on: October 13, 2025
"""

from .transcription_service import TranscriptionService
from .summarization_service import SummarizationService
from ..models import Meeting, Transcript, Summary, ActionItem
from django.utils import timezone
import logging
import traceback
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)


class ProcessingService:
    """
    Service class to orchestrate meeting processing workflow.
    
    This service coordinates:
    - Audio transcription
    - AI-powered summarization
    - Action item extraction
    - Database persistence
    - Error handling and status updates
    
    Attributes:
        meeting_id (int): ID of the meeting to process
        meeting (Meeting): Meeting model instance
        transcription_service (TranscriptionService): Transcription service instance
        summarization_service (SummarizationService): Summarization service instance
    
    Example:
        >>> service = ProcessingService(meeting_id=1)
        >>> success = service.process_meeting()
        >>> if success:
        ...     print("Meeting processed successfully")
    """
    
    def __init__(self, meeting_id: int):
        """
        Initialize processing service with meeting ID.
        
        Args:
            meeting_id (int): ID of the meeting to process
        
        Raises:
            Meeting.DoesNotExist: If meeting with given ID doesn't exist
        """
        self.meeting_id = meeting_id
        
        try:
            self.meeting = Meeting.objects.get(id=meeting_id)
            logger.info(f"ProcessingService initialized for meeting {meeting_id}: '{self.meeting.title}'")
        except Meeting.DoesNotExist:
            logger.error(f"Meeting with ID {meeting_id} does not exist")
            raise
        
        # Initialize AI services
        self.transcription_service = TranscriptionService()
        self.summarization_service = SummarizationService()
    
    def process_meeting(self) -> bool:
        """
        Main method to process entire meeting workflow.
        
        This method executes the complete processing pipeline:
        1. Update status to 'processing'
        2. Transcribe audio file
        3. Save transcript to database
        4. Generate AI summary
        5. Save summary to database
        6. Extract and save action items
        7. Update status to 'completed'
        
        Returns:
            bool: True if processing successful, False if failed
        
        Example:
            >>> service = ProcessingService(meeting_id=1)
            >>> if service.process_meeting():
            ...     print("Processing completed successfully")
            ... else:
            ...     print("Processing failed")
        """
        try:
            logger.info(f"=" * 60)
            logger.info(f"Starting processing for meeting {self.meeting_id}: '{self.meeting.title}'")
            logger.info(f"=" * 60)
            
            # ==========================================
            # STEP 1: Update status to processing
            # ==========================================
            logger.info("STEP 1: Updating meeting status to 'processing'...")
            self.meeting.status = 'processing'
            self.meeting.save()
            logger.info("✓ Status updated successfully")
            
            # ==========================================
            # STEP 2: Transcribe audio
            # ==========================================
            logger.info("STEP 2: Transcribing audio file...")
            audio_path = self.meeting.audio_file.path
            logger.info(f"Audio file path: {audio_path}")
            
            # Get audio duration
            try:
                duration = self.transcription_service.get_audio_duration(audio_path)
                if duration:
                    self.meeting.duration = duration
                    self.meeting.save()
                    logger.info(f"✓ Audio duration: {duration} seconds")
            except Exception as e:
                logger.warning(f"Could not get audio duration: {str(e)}")
            
            transcript_text = self.transcription_service.transcribe_audio(audio_path)
            
            if not transcript_text:
                raise ValueError("Transcription returned empty text")
            
            word_count = len(transcript_text.split())
            logger.info(f"✓ Transcription completed: {word_count} words, {len(transcript_text)} characters")
            
            # ==========================================
            # STEP 3: Save transcript to database
            # ==========================================
            logger.info("STEP 3: Saving transcript to database...")
            transcript = Transcript.objects.create(
                meeting=self.meeting,
                text=transcript_text,
                word_count=word_count
            )
            logger.info(f"✓ Transcript saved with ID: {transcript.id}")
            
            # ==========================================
            # STEP 4: Generate AI summary
            # ==========================================
            logger.info("STEP 4: Generating AI-powered summary...")
            summary_data = self.summarization_service.generate_summary(transcript_text)
            
            if not summary_data:
                raise ValueError("Summarization returned empty data")
            
            logger.info(
                f"✓ Summary generated: "
                f"{len(summary_data.get('key_decisions', []))} decisions, "
                f"{len(summary_data.get('action_items', []))} action items, "
                f"{len(summary_data.get('discussion_topics', []))} topics"
            )
            
            # ==========================================
            # STEP 5: Save summary to database
            # ==========================================
            logger.info("STEP 5: Saving summary to database...")
            summary = Summary.objects.create(
                meeting=self.meeting,
                executive_summary=summary_data.get('executive_summary', ''),
                key_decisions=summary_data.get('key_decisions', []),
                discussion_topics=summary_data.get('discussion_topics', []),
                participants=summary_data.get('participants', []),
                insights=summary_data.get('insights', [])
            )
            logger.info(f"✓ Summary saved with ID: {summary.id}")
            
            # ==========================================
            # STEP 6: Save action items
            # ==========================================
            logger.info("STEP 6: Saving action items to database...")
            action_items = summary_data.get('action_items', [])
            
            if not action_items:
                logger.warning("No action items found in summary")
            else:
                for idx, item_data in enumerate(action_items, 1):
                    try:
                        task_text = item_data.get('task', '')
                        action_item = ActionItem.objects.create(
                            meeting=self.meeting,
                            title=task_text[:300] if task_text else 'Untitled Task',  # Populate title from task
                            task=task_text,
                            assignee=item_data.get('assignee', 'Unassigned'),
                            priority=item_data.get('priority', 'medium'),
                            deadline=item_data.get('deadline')
                        )
                        logger.info(
                            f"  [{idx}/{len(action_items)}] Action item created: "
                            f"'{action_item.task[:50]}...' → {action_item.assignee}"
                        )
                    except Exception as e:
                        logger.error(f"Failed to save action item {idx}: {str(e)}")
                        # Continue with other items even if one fails
                        continue
                
                logger.info(f"✓ {len(action_items)} action items saved")
            
            # ==========================================
            # STEP 7: Mark as completed
            # ==========================================
            logger.info("STEP 7: Marking meeting as completed...")
            self.meeting.status = 'completed'
            self.meeting.updated_at = timezone.now()
            self.meeting.save()
            logger.info("✓ Meeting status updated to 'completed'")
            
            # ==========================================
            # SUCCESS SUMMARY
            # ==========================================
            logger.info(f"=" * 60)
            logger.info(f"✓✓✓ SUCCESSFULLY PROCESSED MEETING {self.meeting_id} ✓✓✓")
            logger.info(f"Meeting: '{self.meeting.title}'")
            logger.info(f"Transcript: {word_count} words")
            logger.info(f"Decisions: {len(summary_data.get('key_decisions', []))}")
            logger.info(f"Action Items: {len(action_items)}")
            logger.info(f"Topics: {len(summary_data.get('discussion_topics', []))}")
            logger.info(f"=" * 60)
            
            return True
        
        except Meeting.DoesNotExist:
            # This shouldn't happen as we check in __init__, but handle it anyway
            error_msg = f"Meeting {self.meeting_id} no longer exists"
            logger.error(error_msg)
            return False
        
        except Exception as e:
            # ==========================================
            # ERROR HANDLING
            # ==========================================
            logger.error(f"=" * 60)
            logger.error(f"✗✗✗ ERROR PROCESSING MEETING {self.meeting_id} ✗✗✗")
            logger.error(f"Meeting: '{self.meeting.title if hasattr(self, 'meeting') else 'Unknown'}'")
            logger.error(f"Error Type: {type(e).__name__}")
            logger.error(f"Error Message: {str(e)}")
            logger.error(f"=" * 60)
            logger.error("Full Traceback:")
            logger.error(traceback.format_exc())
            logger.error(f"=" * 60)
            
            # Update meeting status to failed
            try:
                self.meeting.status = 'failed'
                self.meeting.error_message = str(e)[:500]  # Limit error message length
                self.meeting.updated_at = timezone.now()
                self.meeting.save()
                logger.info(f"Meeting status updated to 'failed'")
            except Exception as save_error:
                logger.error(f"Failed to update meeting status: {str(save_error)}")
            
            return False
    
    def run_in_background(self):
        """
        Wrapper to run processing in separate thread.
        
        This method starts the processing workflow in a background thread,
        allowing the main request to return immediately. Useful for async
        processing of long-running tasks.
        
        Example:
            >>> service = ProcessingService(meeting_id=1)
            >>> service.run_in_background()
            >>> # Processing continues in background
        """
        import threading
        
        logger.info(f"Starting background processing for meeting {self.meeting_id}")
        
        thread = threading.Thread(
            target=self.process_meeting,
            name=f"MeetingProcessor-{self.meeting_id}"
        )
        thread.daemon = True
        thread.start()
        
        logger.info(
            f"Background thread started for meeting {self.meeting_id}: "
            f"{thread.name}"
        )
