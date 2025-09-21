from django.db import models
from django.conf import settings
from events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    is_present = models.BooleanField(default=False, help_text="Mark if the participant was present")

    class Meta:
        # A participant can only have one attendance record per event
        unique_together = ('event', 'participant')
        ordering = ['participant__first_name']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"Attendance for {self.participant.username} at {self.event.event_name} - {status}"

class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_given')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (Poor) to 5 (Excellent)"
    )
    comments = models.TextField(blank=True, null=True, help_text="What did you like or dislike?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A participant can only leave one piece of feedback per event
        unique_together = ('event', 'participant')
        ordering = ['-created_at']
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"Feedback from {self.participant.username} for {self.event.event_name}"
