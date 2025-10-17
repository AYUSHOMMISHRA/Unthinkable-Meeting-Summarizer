"""
Django views for Meeting Summarizer application.

This module contains function-based views for handling:
- File upload and meeting creation
- Processing status tracking
- Meeting detail display
- Meeting list with filtering
- Meeting deletion
- AJAX status endpoint

Created on: October 13, 2025
"""

# ============================================
# 1. IMPORT REQUIRED MODULES
# ============================================
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from .models import Meeting, Transcript, Summary, ActionItem
from .forms import MeetingUploadForm
from .services.processing_service import ProcessingService
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)


# ============================================
# 2. INDEX VIEW (GET/POST)
# ============================================

@require_http_methods(["GET", "POST"])
def index(request):
    """
    Render the main upload page and handle file uploads.
    
    GET: Display upload form
    POST: Process uploaded file and create meeting record
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered upload page with form or JSON response for AJAX
        
    Template:
        meetings/index.html
        
    Context:
        form: MeetingUploadForm instance
    """
    if request.method == 'GET':
        form = MeetingUploadForm()
        return render(request, 'meetings/index.html', {'form': form})
    
    # POST request - handle file upload
    try:
        form = MeetingUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the meeting instance
            meeting = form.save(commit=False)
            
            # Extract title from POST or use filename
            if 'title' in request.POST and request.POST['title'].strip():
                meeting.title = request.POST['title'].strip()
            else:
                # Use filename without extension as title
                filename = meeting.audio_file.name
                meeting.title = os.path.splitext(os.path.basename(filename))[0]
            
            # Set initial status
            meeting.status = 'pending'
            
            # Get file size
            if meeting.audio_file:
                meeting.file_size = meeting.audio_file.size
            
            # Save the meeting
            meeting.save()
            print(f"🔍 DEBUG: Meeting saved with ID: {meeting.id}, Title: {meeting.title}")
            
            # Start processing in background
            try:
                print(f"🔍 DEBUG: Creating ProcessingService for meeting {meeting.id}")
                processor = ProcessingService(meeting.id)  # Pass meeting_id to constructor
                print(f"🔍 DEBUG: Starting background processing...")
                processor.run_in_background()  # No arguments needed
                print(f"🔍 DEBUG: Background processing started successfully for meeting {meeting.id}")
                
                # Add success message
                messages.success(
                    request,
                    f'Meeting "{meeting.title}" uploaded successfully! Processing has started.'
                )
            except Exception as proc_error:
                # Meeting saved but processing failed to start
                print(f"❌ DEBUG ERROR: Failed to start processing - {str(proc_error)}")
                import traceback
                traceback.print_exc()
                messages.warning(
                    request,
                    f'Meeting uploaded but processing failed to start: {str(proc_error)}'
                )
            
            # Check if this is an AJAX request
            print(f"🔍 DEBUG: Checking if AJAX request...")
            print(f"🔍 DEBUG: X-Requested-With header: {request.headers.get('X-Requested-With')}")
            print(f"🔍 DEBUG: All headers: {dict(request.headers)}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print(f"🔍 DEBUG: This is an AJAX request - returning JSON")
                # Return JSON response for AJAX
                return JsonResponse({
                    'success': True,
                    'redirect_url': f'/processing/{meeting.id}/',
                    'message': f'Meeting "{meeting.title}" uploaded successfully!'
                })
            
            print(f"🔍 DEBUG: Not an AJAX request - redirecting normally")
            # Regular form submission - redirect to processing page
            return redirect('meetings:processing', meeting_id=meeting.id)
        
        else:
            # Form is invalid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return JSON error for AJAX
                errors = {field: error[0] for field, error in form.errors.items()}
                return JsonResponse({
                    'success': False,
                    'errors': errors
                }, status=400)
            
            # Regular form submission - re-render with errors
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'meetings/index.html', {'form': form})
    
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
        
        messages.error(request, f'Error uploading file: {str(e)}')
        form = MeetingUploadForm()
        return render(request, 'meetings/index.html', {'form': form})


# ============================================
# 3. UPLOAD MEETING VIEW (GET, POST)
# ============================================

@require_http_methods(["GET", "POST"])
def upload_meeting(request):
    """
    Handle file upload and meeting creation.
    
    GET: Display upload form
    POST: Process uploaded file and create meeting record
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Redirect to processing page on success,
                     re-render form with errors on failure
                     
    Template:
        meetings/index.html (on GET or validation error)
        
    Redirects:
        processing view with meeting ID on success
    """
    if request.method == 'GET':
        form = MeetingUploadForm()
        return render(request, 'meetings/index.html', {'form': form})
    
    # POST request
    try:
        form = MeetingUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the meeting instance
            meeting = form.save(commit=False)
            
            # Extract title from POST or use filename
            if 'title' in request.POST and request.POST['title'].strip():
                meeting.title = request.POST['title'].strip()
            else:
                # Use filename without extension as title
                filename = meeting.audio_file.name
                meeting.title = os.path.splitext(os.path.basename(filename))[0]
            
            # Set initial status
            meeting.status = 'pending'
            
            # Get file size
            if meeting.audio_file:
                meeting.file_size = meeting.audio_file.size
            
            # Save the meeting
            meeting.save()
            
            # Start processing in background
            try:
                processor = ProcessingService(meeting.id)  # Pass meeting_id to constructor
                processor.run_in_background()  # No arguments needed
                
                # Add success message
                messages.success(
                    request,
                    f'Meeting "{meeting.title}" uploaded successfully! Processing has started.'
                )
            except Exception as proc_error:
                # Meeting saved but processing failed to start
                messages.warning(
                    request,
                    f'Meeting uploaded but processing failed to start: {str(proc_error)}'
                )
            
            # Redirect to processing page
            return redirect('processing', meeting_id=meeting.id)
        
        else:
            # Form is invalid - re-render with errors
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'meetings/index.html', {'form': form})
    
    except Exception as e:
        messages.error(request, f'Error uploading file: {str(e)}')
        form = MeetingUploadForm()
        return render(request, 'meetings/index.html', {'form': form})


# ============================================
# 4. PROCESSING VIEW (GET)
# ============================================

def processing(request, meeting_id):
    """
    Display processing status page for a meeting.
    
    Shows a loading/processing interface while the meeting audio
    is being transcribed and summarized.
    
    Args:
        request: HTTP request object
        meeting_id: ID of the meeting being processed
        
    Returns:
        HttpResponse: Rendered processing page
        
    Template:
        meetings/processing.html
        
    Context:
        meeting: Meeting instance
        
    Raises:
        Http404: If meeting with given ID doesn't exist
    """
    try:
        meeting = get_object_or_404(Meeting, id=meeting_id)
        
        context = {
            'meeting': meeting,
            'meeting_id': meeting_id,
        }
        
        return render(request, 'meetings/processing.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading processing page: {str(e)}')
        return redirect('index')


# ============================================
# 5. MEETING DETAIL VIEW (GET)
# ============================================

def meeting_detail(request, meeting_id):
    """
    Display meeting details with transcript, summary, and action items.
    
    Shows the complete results of meeting processing including:
    - Full transcript
    - AI-generated summary
    - Extracted action items
    
    Args:
        request: HTTP request object
        meeting_id: ID of the meeting to display
        
    Returns:
        HttpResponse: Rendered detail page or redirect if not complete
        
    Template:
        meetings/detail.html
        
    Context:
        meeting: Meeting instance
        transcript: Transcript instance (if exists)
        summary: Summary instance (if exists)
        action_items: QuerySet of ActionItem instances
        has_transcript: Boolean
        has_summary: Boolean
        has_action_items: Boolean
        
    Raises:
        Http404: If meeting with given ID doesn't exist
    """
    try:
        meeting = get_object_or_404(Meeting, id=meeting_id)
        
        logger.info(f"Loading meeting detail for meeting ID: {meeting_id}, status: {meeting.status}")
        
        # Check if processing is complete
        if meeting.status != 'completed':
            messages.warning(
                request,
                'Meeting is still being processed. Please wait...'
            )
            return redirect('meetings:processing', meeting_id=meeting.id)
        
        # Get related transcript (if exists)
        transcript = None
        try:
            transcript = meeting.transcripts.first()
            logger.info(f"Transcript found: {transcript is not None}")
        except Transcript.DoesNotExist:
            logger.warning(f"No transcript found for meeting {meeting_id}")
            pass
        except Exception as e:
            logger.error(f"Error fetching transcript for meeting {meeting_id}: {str(e)}")
        
        # Get related summary (if exists)
        summary = None
        try:
            if hasattr(meeting, 'summary'):
                summary = meeting.summary
                logger.info(f"Summary found: {summary is not None}")
        except Summary.DoesNotExist:
            logger.warning(f"No summary found for meeting {meeting_id}")
            pass
        except Exception as e:
            logger.error(f"Error fetching summary for meeting {meeting_id}: {str(e)}")
        
        # Get all action items ordered by priority
        action_items = meeting.action_items.all().order_by('-priority', 'deadline')
        logger.info(f"Action items count: {action_items.count()}")
        
        # Get tags for this meeting
        tags = meeting.tags.all()
        
        # Get related meetings (limit to 3 most recent)
        related_meetings = meeting.related_meetings.filter(status='completed').order_by('-created_at')[:3]
        
        context = {
            'meeting': meeting,
            'transcript': transcript,
            'summary': summary,
            'action_items': action_items,
            'tags': tags,
            'related_meetings': related_meetings,
            'has_transcript': transcript is not None,
            'has_summary': summary is not None,
            'has_action_items': action_items.exists(),
            'has_tags': tags.exists(),
            'has_related_meetings': related_meetings.exists(),
        }
        
        return render(request, 'meetings/detail.html', context)
    
    except Exception as e:
        logger.error(f"Error in meeting_detail view for meeting {meeting_id}: {str(e)}")
        logger.exception(e)  # This will log the full traceback
        messages.error(request, f'Error loading meeting details: {str(e)}')
        return redirect('meetings:list')


# ============================================
# 6. MEETINGS LIST VIEW (GET)
# ============================================

def meetings_list(request):
    """
    Display paginated list of all meetings with filtering and search.
    
    Supports:
    - Filtering by status (query param: status)
    - Search by title (query param: search)
    - Pagination (9 meetings per page)
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered list page
        
    Template:
        meetings/list.html
        
    Context:
        meetings: Paginated meetings
        page_obj: Paginator page object
        status_filter: Current status filter
        search_query: Current search query
        total_count: Total number of meetings
        
    Query Parameters:
        status (str): Filter by status (pending/processing/completed/failed)
        search (str): Search by meeting title
        page (int): Page number for pagination
    """
    try:
        # Get all meetings
        # Use select_related and prefetch_related to optimize queries
        meetings = Meeting.objects.select_related('summary').prefetch_related(
            'transcripts', 'action_items'
        )
        
        # Get filter and search parameters
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('search', '')
        filter_type = request.GET.get('filter', 'all')  # all, recent, starred
        sort_by = request.GET.get('sort', 'date-desc')  # date-desc, date-asc, title-asc, title-desc, duration-desc, duration-asc
        
        # Apply status filter if provided
        if status_filter and status_filter in ['pending', 'processing', 'completed', 'failed']:
            meetings = meetings.filter(status=status_filter)
        
        # Apply filter type
        if filter_type == 'starred':
            meetings = meetings.filter(is_starred=True)
        elif filter_type == 'recent':
            # Recent = last 7 days
            from datetime import timedelta
            seven_days_ago = timezone.now() - timedelta(days=7)
            meetings = meetings.filter(created_at__gte=seven_days_ago)
        # 'all' means no additional filter
        
        # Apply search filter if provided
        if search_query:
            meetings = meetings.filter(title__icontains=search_query)
        
        # Apply sorting
        if sort_by == 'date-desc':
            meetings = meetings.order_by('-created_at')
        elif sort_by == 'date-asc':
            meetings = meetings.order_by('created_at')
        elif sort_by == 'title-asc':
            meetings = meetings.order_by('title')
        elif sort_by == 'title-desc':
            meetings = meetings.order_by('-title')
        elif sort_by == 'duration-desc':
            meetings = meetings.order_by('-duration')
        elif sort_by == 'duration-asc':
            meetings = meetings.order_by('duration')
        else:
            meetings = meetings.order_by('-created_at')
        
        # Get total count before pagination
        total_count = meetings.count()
        
        # Paginate results (9 per page)
        paginator = Paginator(meetings, 9)
        page_number = request.GET.get('page', 1)
        
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page
            page_obj = paginator.page(paginator.num_pages)
        
        # Calculate statistics from all meetings (not just paginated)
        all_meetings = Meeting.objects.all()
        total_duration = sum(m.duration for m in all_meetings if m.duration)
        
        # Calculate total participants (safely handle missing summaries)
        total_participants = 0
        for m in all_meetings:
            if hasattr(m, 'summary') and m.summary and m.summary.participants:
                total_participants += len(m.summary.participants)
        
        # Calculate total action items from ActionItem model
        total_action_items = ActionItem.objects.filter(meeting__in=all_meetings).count()
        
        # Convert total_duration from seconds to hours
        total_duration_hours = total_duration / 3600 if total_duration else 0
        
        context = {
            'meetings': page_obj,
            'page_obj': page_obj,
            'status_filter': status_filter,
            'search_query': search_query,
            'filter_type': filter_type,
            'sort_by': sort_by,
            'total_count': total_count,
            'paginator': paginator,
            'total_duration_hours': total_duration_hours,
            'total_participants': total_participants,
            'total_action_items': total_action_items,
        }
        
        return render(request, 'meetings/list.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading meetings list: {str(e)}')
        return render(request, 'meetings/list.html', {
            'meetings': [],
            'total_count': 0,
        })


# ============================================
# 7. DELETE MEETING VIEW (POST)
# ============================================

@require_http_methods(["POST"])
def delete_meeting(request, meeting_id):
    """
    Delete a meeting and its associated audio file.
    
    Removes:
    - Meeting record from database
    - Associated audio file from filesystem
    - All related records (transcript, summary, action items) via CASCADE
    
    Args:
        request: HTTP request object
        meeting_id: ID of the meeting to delete
        
    Returns:
        HttpResponse: Redirect to meetings list
        
    Redirects:
        meetings_list view with success message
        
    Raises:
        Http404: If meeting with given ID doesn't exist
    """
    try:
        meeting = get_object_or_404(Meeting, id=meeting_id)
        
        # Store title for success message
        meeting_title = meeting.title
        
        # Delete audio file from filesystem
        if meeting.audio_file:
            try:
                if os.path.isfile(meeting.audio_file.path):
                    os.remove(meeting.audio_file.path)
            except Exception as file_error:
                # Log error but continue with database deletion
                print(f"Error deleting file: {file_error}")
        
        # Delete meeting from database (CASCADE will delete related records)
        meeting.delete()
        
        # Add success message
        messages.success(
            request,
            f'Meeting "{meeting_title}" has been deleted successfully.'
        )
        
        return redirect('meetings_list')
    
    except Exception as e:
        messages.error(request, f'Error deleting meeting: {str(e)}')
        return redirect('meetings_list')


# ============================================
# 8. GET MEETING STATUS VIEW (GET) - AJAX ENDPOINT
# ============================================

def get_meeting_status(request, meeting_id):
    """
    AJAX endpoint to get current meeting processing status.
    
    Returns JSON with:
    - status: Current processing status
    - percentage: Estimated completion percentage
    - error_message: Error details if status is 'failed'
    
    Args:
        request: HTTP request object
        meeting_id: ID of the meeting
        
    Returns:
        JsonResponse: JSON object with status information
        
    JSON Response:
        {
            'status': 'pending'|'processing'|'completed'|'failed',
            'percentage': 0-100,
            'error_message': 'Error details' (if failed),
            'meeting_id': int,
            'title': 'Meeting title'
        }
        
    Status Codes:
        200: Success
        404: Meeting not found (JSON response)
        500: Server error (JSON response)
    """
    try:
        meeting = get_object_or_404(Meeting, id=meeting_id)
        
        # Calculate percentage based on status
        percentage_map = {
            'pending': 10,
            'processing': 50,
            'completed': 100,
            'failed': 0,
        }
        
        percentage = percentage_map.get(meeting.status, 0)
        
        # Build response data
        response_data = {
            'status': meeting.status,
            'percentage': percentage,
            'meeting_id': meeting.id,
            'title': meeting.title,
        }
        
        # Include error message if status is failed
        if meeting.status == 'failed':
            response_data['error_message'] = meeting.error_message or 'Processing failed. Please try again.'
        
        return JsonResponse(response_data)
    
    except Meeting.DoesNotExist:
        return JsonResponse({
            'error': 'Meeting not found',
            'status': 'error',
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'error': f'Error retrieving status: {str(e)}',
            'status': 'error',
        }, status=500)


# ============================================
# 9. TOGGLE STAR VIEW (POST) - AJAX ENDPOINT
# ============================================

@require_http_methods(["POST"])
def toggle_star(request, meeting_id):
    """
    Toggle the starred/favorite status of a meeting.
    
    Args:
        request: HTTP request object
        meeting_id: ID of the meeting to toggle
        
    Returns:
        JsonResponse: JSON object with new status
        
    JSON Response:
        {
            'success': True,
            'is_starred': True|False,
            'message': 'Meeting starred'|'Meeting unstarred'
        }
        
    Status Codes:
        200: Success
        404: Meeting not found
        500: Server error
    """
    try:
        meeting = get_object_or_404(Meeting, id=meeting_id)
        
        # Toggle the starred status
        meeting.is_starred = not meeting.is_starred
        meeting.save()
        
        return JsonResponse({
            'success': True,
            'is_starred': meeting.is_starred,
            'message': 'Meeting starred' if meeting.is_starred else 'Meeting unstarred'
        })
    
    except Meeting.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Meeting not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error toggling star: {str(e)}'
        }, status=500)


def about(request):
    """
    Display the About page with project information.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Rendered about page
    """
    return render(request, 'meetings/about.html')
