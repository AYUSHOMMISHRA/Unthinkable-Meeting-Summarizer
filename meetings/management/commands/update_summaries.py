"""
Management command to update existing summaries with missing fields.
"""
from django.core.management.base import BaseCommand
from meetings.models import Summary

class Command(BaseCommand):
    help = 'Update existing summaries to add missing participants and insights fields'

    def handle(self, *args, **options):
        summaries = Summary.objects.all()
        updated_count = 0
        
        for summary in summaries:
            needs_update = False
            
            # Check if participants field is None or missing
            if summary.participants is None:
                summary.participants = []
                needs_update = True
            
            # Check if insights field is None or missing
            if summary.insights is None:
                summary.insights = []
                needs_update = True
            
            if needs_update:
                summary.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated summary {summary.id} for meeting "{summary.meeting.title}"')
                )
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully updated {updated_count} summaries')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All summaries already have participants and insights fields')
            )
