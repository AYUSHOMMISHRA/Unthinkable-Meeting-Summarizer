"""
Debug views to help diagnose meeting data issues.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Meeting, Transcript, Summary, ActionItem


@require_GET
def debug_meeting(request, meeting_id):
    """
    Debug endpoint to check meeting data.
    
    Returns JSON with all meeting information to help diagnose issues.
    """
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        
        # Get transcript count
        transcript_count = meeting.transcripts.count()
        transcript_data = None
        if transcript_count > 0:
            transcript = meeting.transcripts.first()
            transcript_data = {
                'id': transcript.id,
                'word_count': transcript.word_count,
                'language': transcript.language,
                'text_length': len(transcript.text) if transcript.text else 0,
                'created_at': str(transcript.created_at)
            }
        
        # Get summary
        summary_data = None
        try:
            if hasattr(meeting, 'summary'):
                summary = meeting.summary
                summary_data = {
                    'id': summary.id,
                    'executive_summary_length': len(summary.executive_summary) if summary.executive_summary else 0,
                    'key_decisions_count': len(summary.key_decisions) if summary.key_decisions else 0,
                    'discussion_topics_count': len(summary.discussion_topics) if summary.discussion_topics else 0,
                    'created_at': str(summary.created_at)
                }
        except Summary.DoesNotExist:
            summary_data = {'error': 'Summary does not exist'}
        
        # Get action items
        action_items = meeting.action_items.all()
        action_items_data = []
        for item in action_items:
            action_items_data.append({
                'id': item.id,
                'title': item.title[:50] if item.title else 'N/A',
                'task': item.task[:100] if item.task else 'N/A',
                'assignee': item.assignee,
                'priority': item.priority,
                'is_completed': item.is_completed
            })
        
        debug_info = {
            'meeting': {
                'id': meeting.id,
                'title': meeting.title,
                'status': meeting.status,
                'duration': meeting.duration,
                'file_size': meeting.file_size,
                'created_at': str(meeting.created_at),
                'updated_at': str(meeting.updated_at),
                'error_message': meeting.error_message
            },
            'transcript': {
                'count': transcript_count,
                'data': transcript_data
            },
            'summary': summary_data,
            'action_items': {
                'count': len(action_items_data),
                'data': action_items_data
            }
        }
        
        return JsonResponse(debug_info, json_dumps_params={'indent': 2})
        
    except Meeting.DoesNotExist:
        return JsonResponse({
            'error': f'Meeting with ID {meeting_id} does not exist'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'type': type(e).__name__
        }, status=500)
