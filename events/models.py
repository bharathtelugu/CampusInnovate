from django.db import models
from django.conf import settings

# This model is central and will be linked to by almost all other models.
class Event(models.Model):
    MODE_CHOICES = (
        ('physical', 'Physical'),
        ('virtual', 'Virtual'),
        ('hybrid', 'Hybrid'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    # Core Details
    event_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, help_text="Short tagline for the event")
    about_event = models.TextField(help_text="Detailed description of the event.")
    
    # Timelines
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()

    # Configuration
    event_mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Venue (for physical/hybrid events)
    venue_name = models.CharField(max_length=255, blank=True, null=True)
    venue_google_map_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.event_name

# --- Event-Related Subtables ---
# These models are all linked to a specific Event via a ForeignKey.

class ProblemStatement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='problem_statements')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules')
    day_number = models.PositiveIntegerField(default=1)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True, help_text="Overview for the day")

    class Meta:
        ordering = ['date', 'day_number']

    def __str__(self):
        return f"{self.event.event_name} - Day {self.day_number}"

class SubSchedule(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='sub_schedules')
    time_start = models.TimeField()
    time_end = models.TimeField()
    activity_description = models.CharField(max_length=255)

    class Meta:
        ordering = ['time_start']

class FAQ(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

class EventMedia(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='media')
    banner_image = models.ImageField(upload_to='event_banners/')
    logo = models.ImageField(upload_to='event_logos/', blank=True, null=True)

# This model links staff users (Judges, Managers, etc.) to specific events with specific roles.
class EventStaff(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_roles')
    role = models.CharField(max_length=50, help_text="e.g., Lead Organizer, Judge, Mentor, Volunteer")
    
    class Meta:
        unique_together = ('event', 'user', 'role')

    def __str__(self):
        return f"{self.user.username} as {self.role} for {self.event.event_name}"

# These are additional informational models you designed
class Eligibility(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eligibility_criteria')
    description = models.TextField()

class HowToParticipate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participation_steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    class Meta:
        ordering = ['step_number']

class CertificatesAndRewards(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rewards')
    title = models.CharField(max_length=255)
    description = models.TextField()

class EventResource(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='event_resources/')
