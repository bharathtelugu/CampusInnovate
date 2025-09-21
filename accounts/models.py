from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from events.models import Event # Import Event model

# --- UPDATED USER MODEL ---
# We've removed site_role. It's simpler now.
# is_staff=False (default) == Participant
# is_staff=True == Privileged user (Judge, Manager, etc.)
class User(AbstractUser):
    # No role field needed here. We use Django Groups.
    pass

# --- UNCHANGED USERPROFILE MODEL ---
# This model is still perfect.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Student-specific fields
    student_roll_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    
    # General & Professional fields
    about = models.TextField(blank=True, null=True)
    highlight = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="General skills: design, development")
    technical_skillset = models.TextField(blank=True, null=True, help_text="Langs, frameworks, tools")
    social_links = models.JSONField(default=dict, blank=True)
    professional_role = models.CharField(max_length=100, blank=True, null=True, help_text="For judges/mentors")
    organization_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# --- NEW MODEL: RegistrationCode (Table: InviteCode) ---
# Your model for gating participant sign-ups
class RegistrationCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, 
                              help_text="If null, this is a global campus-wide code.")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                   related_name="created_codes")
    
    max_uses = models.PositiveIntegerField(default=1, help_text="How many times this code can be used.")
    uses_count = models.PositiveIntegerField(default=0)
    
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.uses_count}/{self.max_uses} used)"

# --- NEW MODEL: EventRegistration (Optional but Recommended) ---
# Your model for explicitly linking a participant to an event
class EventRegistration(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                    related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, 
                              related_name="participants")
    
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('participant', 'event') # User can only register for an event once

    def __str__(self):
        return f"{self.participant.username} registered for {self.event.event_name}"

# --- NEW MODEL: ParticipantRegistrationLog ---
# Your model for auditing sign-up attempts
class ParticipantRegistrationLog(models.Model):
    email_attempt = models.EmailField()
    code_used = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('fail', 'Failed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reason = models.CharField(max_length=255, blank=True, null=True, 
                              help_text="e.g., Code expired, Code invalid, Email exists")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email_attempt} at {self.timestamp} - {self.status}"