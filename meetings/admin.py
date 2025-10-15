"""
Django admin configuration for Meeting Summarizer application.

This module configures the admin interface for managing meetings,
transcripts, summaries, and action items with custom displays,
filters, and bulk actions.

Created on: October 13, 2025
"""

# ============================================
# 1. IMPORT MODELS AND ADMIN MODULE
# ============================================
from django.contrib import admin
from django.utils.html import format_html
from .models import Meeting, Transcript, Summary, ActionItem, Tag


# ============================================
# 2. MEETING ADMIN CLASS
# ============================================

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Meeting model.
    
    Features:
    - List display with title, status, duration, file size
    - Filtering by status and creation date
    - Search by meeting title
    - Read-only timestamp and metadata fields
    - Date hierarchy for easy navigation
    - Custom bulk actions for status updates
    - Custom display methods with formatting
    """
    
    # List view configuration
    list_display = [
        'title',
        'status',
        'duration',
        'created_at',
        'file_size_display',
    ]
    
    list_filter = [
        'status',
        'created_at',
    ]
    
    search_fields = [
        'title',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'file_size',
        'duration',
    ]
    
    list_per_page = 20
    
    date_hierarchy = 'created_at'
    
    # Custom actions
    actions = [
        'mark_as_completed',
        'mark_as_failed',
    ]
    
    # Fieldsets for organized edit form
    fieldsets = (
        ('Meeting Information', {
            'fields': ('title', 'audio_file', 'notes', 'is_starred')
        }),
        ('Organization', {
            'fields': ('tags', 'related_meetings')
        }),
        ('Processing Status', {
            'fields': ('status', 'error_message')
        }),
        ('Metadata', {
            'fields': ('duration', 'file_size', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Many-to-many fields configuration
    filter_horizontal = ['tags', 'related_meetings']
    
    def file_size_display(self, obj):
        """
        Display formatted file size.
        
        Args:
            obj (Meeting): Meeting instance
            
        Returns:
            str: Formatted file size (e.g., "2.50 MB" or "500 KB")
        """
        return obj.get_file_size_display()
    file_size_display.short_description = 'File Size'
    
    def mark_as_completed(self, request, queryset):
        """
        Bulk action to mark selected meetings as completed.
        
        Args:
            request: HTTP request object
            queryset: Selected Meeting objects
        """
        updated = queryset.update(status='completed')
        self.message_user(
            request,
            f'{updated} meeting(s) successfully marked as completed.'
        )
    mark_as_completed.short_description = 'Mark selected meetings as completed'
    
    def mark_as_failed(self, request, queryset):
        """
        Bulk action to mark selected meetings as failed.
        
        Args:
            request: HTTP request object
            queryset: Selected Meeting objects
        """
        updated = queryset.update(status='failed')
        self.message_user(
            request,
            f'{updated} meeting(s) marked as failed.'
        )
    mark_as_failed.short_description = 'Mark selected meetings as failed'


# ============================================
# 3. TRANSCRIPT ADMIN CLASS
# ============================================

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Transcript model.
    
    Features:
    - List display with meeting, language, word count
    - Filtering by language and creation date
    - Search by meeting title and transcript text
    - Read-only word count and timestamp fields
    """
    
    list_display = [
        'meeting',
        'language',
        'word_count',
        'created_at',
    ]
    
    list_filter = [
        'language',
        'created_at',
    ]
    
    search_fields = [
        'meeting__title',
        'text',
    ]
    
    readonly_fields = [
        'word_count',
        'created_at',
    ]
    
    # Fieldsets for organized edit form
    fieldsets = (
        ('Transcript Information', {
            'fields': ('meeting', 'text', 'language')
        }),
        ('Statistics', {
            'fields': ('word_count', 'confidence_score'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ============================================
# 4. SUMMARY ADMIN CLASS
# ============================================

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Summary model.
    
    Features:
    - List display with meeting and creation date
    - Search by meeting title and summary text
    - Read-only timestamp fields
    - Organized fieldsets for structured data
    """
    
    list_display = [
        'meeting',
        'created_at',
    ]
    
    search_fields = [
        'meeting__title',
        'executive_summary',
    ]
    
    readonly_fields = [
        'created_at',
    ]
    
    # Fieldsets for organized edit form
    fieldsets = (
        ('Summary Information', {
            'fields': ('meeting', 'executive_summary')
        }),
        ('Structured Data', {
            'fields': ('key_decisions', 'discussion_topics', 'participants', 'insights'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ============================================
# 5. ACTION ITEM ADMIN CLASS
# ============================================

@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for ActionItem model.
    
    Features:
    - List display with all key fields
    - Filtering by priority, completion status, and deadline
    - Search by task, assignee, and meeting title
    - Inline editing of completion status
    - Bulk actions for marking complete/incomplete
    """
    
    list_display = [
        'task',
        'meeting',
        'assignee',
        'priority',
        'deadline',
        'is_completed',
    ]
    
    list_filter = [
        'priority',
        'is_completed',
        'deadline',
    ]
    
    search_fields = [
        'task',
        'assignee',
        'meeting__title',
    ]
    
    list_editable = [
        'is_completed',
    ]
    
    # Custom bulk actions
    actions = [
        'mark_completed',
        'mark_incomplete',
    ]
    
    # Fieldsets for organized edit form
    fieldsets = (
        ('Action Item Details', {
            'fields': ('meeting', 'task', 'assignee')
        }),
        ('Priority & Deadline', {
            'fields': ('priority', 'deadline', 'is_completed')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'created_at',
        'completed_at',
    ]
    
    def mark_completed(self, request, queryset):
        """
        Bulk action to mark selected action items as completed.
        
        Args:
            request: HTTP request object
            queryset: Selected ActionItem objects
        """
        updated = 0
        for item in queryset.filter(is_completed=False):
            item.mark_completed()
            updated += 1
        
        self.message_user(
            request,
            f'{updated} action item(s) successfully marked as completed.'
        )
    mark_completed.short_description = 'Mark selected as completed'
    
    def mark_incomplete(self, request, queryset):
        """
        Bulk action to mark selected action items as incomplete.
        
        Args:
            request: HTTP request object
            queryset: Selected ActionItem objects
        """
        updated = 0
        for item in queryset.filter(is_completed=True):
            item.mark_incomplete()
            updated += 1
        
        self.message_user(
            request,
            f'{updated} action item(s) marked as incomplete.'
        )
    mark_incomplete.short_description = 'Mark selected as incomplete'


# ============================================
# 6. TAG ADMIN CLASS
# ============================================

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Tag model.
    
    Features:
    - List display with name and color preview
    - Search by tag name
    - Custom color display with visual preview
    """
    
    # List view configuration
    list_display = [
        'name',
        'color_preview',
        'created_at',
        'meeting_count',
    ]
    
    search_fields = ['name']
    
    readonly_fields = ['created_at']
    
    def color_preview(self, obj):
        """
        Display color preview swatch in admin list.
        
        Args:
            obj: Tag instance
            
        Returns:
            str: HTML with color preview
        """
        return format_html(
            '<div style="width: 40px; height: 20px; background-color: {}; border: 1px solid #ddd; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def meeting_count(self, obj):
        """
        Display count of meetings using this tag.
        
        Args:
            obj: Tag instance
            
        Returns:
            int: Number of meetings with this tag
        """
        return obj.meetings.count()
    meeting_count.short_description = 'Meetings'


# ============================================
# 7. REGISTER ALL MODELS WITH ADMIN CLASSES
# ============================================
# Note: Models are registered using @admin.register() decorators above
# This provides a cleaner syntax than admin.site.register()

# The following models are registered:
# - Meeting (with MeetingAdmin)
# - Transcript (with TranscriptAdmin)
# - Summary (with SummaryAdmin)
# - ActionItem (with ActionItemAdmin)
# - Tag (with TagAdmin)

