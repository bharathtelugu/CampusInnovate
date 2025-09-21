from django.db import models
from django.conf import settings
from events.models import Event

class Notification(models.Model):
    """
    Represents a notification sent to a single user.
    These are typically system-generated (e.g., team invite, submission reminder).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.URLField(blank=True, null=True, help_text="A link to the relevant page (e.g., team dashboard).")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}..."

class Announcement(models.Model):
    """
    Represents an announcement made for a specific event.
    Visible to all participants of that event.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Announcement for {self.event.event_name}: {self.title}"
