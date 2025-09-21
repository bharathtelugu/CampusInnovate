from django.contrib import admin
from .models import Notification, Announcement

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin view for notifications. These are system-generated,
    so the admin interface is primarily for auditing/viewing.
    """
    list_display = ('user', 'message', 'is_read', 'created_at', 'link')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('user', 'message', 'link', 'is_read', 'created_at')

    def has_add_permission(self, request):
        # Notifications should not be manually created by admins
        return False

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Admin view for announcements.
    Allows staff to create and manage event-specific announcements.
    """
    list_display = ('title', 'event', 'created_at')
    list_filter = ('event',)
    search_fields = ('title', 'event__event_name')
