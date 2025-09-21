from django.contrib import admin
from .models import Attendance, Feedback
from import_export.admin import ImportExportModelAdmin

@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    """
    Admin view for managing participant attendance.
    Allows for easy filtering and bulk editing.
    """
    list_display = ('participant', 'event', 'is_present', 'check_in_time', 'check_out_time')
    list_filter = ('event', 'is_present')
    search_fields = ('participant__username', 'participant__first_name', 'participant__last_name', 'event__event_name')
    list_editable = ('is_present',)
    autocomplete_fields = ('participant', 'event')
    # Enables exporting attendance lists to CSV/Excel
    resource_class = None 

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin view for viewing participant feedback.
    This view should be read-only for data integrity.
    """
    list_display = ('participant', 'event', 'rating', 'created_at')
    list_filter = ('event', 'rating')
    search_fields = ('participant__username', 'event__event_name', 'comments')
    readonly_fields = ('participant', 'event', 'rating', 'comments', 'created_at')
    autocomplete_fields = ('participant', 'event')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
