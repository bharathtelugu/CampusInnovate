from django.db import models
from django.conf import settings

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, help_text="Short tagline for the event")
    hero_section_details = models.TextField()
    
    # Timelines
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()

    # Event Details
    event_mode = models.CharField(max_length=10, choices=[('physical', 'Physical'), ('virtual', 'Virtual'), ('hybrid', 'Hybrid')])
    why_participate = models.TextField()
    what_is_event = models.TextField()
    about_event = models.TextField()
    benefits = models.TextField()

    # Venue
    venue_name = models.CharField(max_length=255, blank=True, null=True)
    venue_location = models.CharField(max_length=255, blank=True, null=True)
    venue_google_map_link = models.URLField(blank=True, null=True)

    # Contact
    contact_email = models.EmailField(blank=True, null=True)
    contact_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    contact_instagram = models.URLField(blank=True, null=True)
    contact_linkedin = models.URLField(blank=True, null=True)
    
    registration_link = models.URLField(blank=True, null=True, help_text="External registration link (if any)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.event_name

# --- Event-Related Subtables ---

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
    logo = models.ImageField(upload_to='event_logos/')
    gallery = models.JSONField(default=list, blank=True, help_text="List of image/video URLs")

# This is the new, refined table for Organizers/Judges/Volunteers
class EventStaff(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_roles')
    role = models.CharField(max_length=50, help_text="e.g., Lead Organizer, Judge, Mentor, Volunteer")
    
    class Meta:
        unique_together = ('event', 'user', 'role') # A user can have multiple roles in one event if needed, or just one

    def __str__(self):
        return f"{self.user.username} as {self.role} for {self.event.event_name}"
        
# ... and so on for all your other tables (Eligibility, HowToParticipate, Resources, etc.)