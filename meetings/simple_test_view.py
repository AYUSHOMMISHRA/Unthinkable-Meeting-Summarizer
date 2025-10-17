from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def simple_meeting_test(request, meeting_id):
    """
    Simple test endpoint to verify routing works without any database queries.
    """
    return JsonResponse({
        'message': f'Meeting ID {meeting_id} route is working!',
        'meeting_id': meeting_id,
        'test': 'success'
    })
