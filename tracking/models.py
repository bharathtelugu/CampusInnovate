from django.db import models
from django.conf import settings
from events.models import Event

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance')
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('event', 'participant')

    def __str__(self):
        return f"Attendance for {self.participant.username} at {self.event.event_name}"

class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_given')
    rating = models.PositiveIntegerField(help_text="Rating from 1 to 5")
    comments = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('event', 'participant')
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"Feedback from {self.participant.username} for {self.event.event_name}"