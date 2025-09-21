from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# The events model is referenced by RegistrationCode and EventRegistration
# It's assumed to be in an app named 'events'
from events.models import Event 

# --- 1. Custom User Model ---
# We use Django's built-in Groups for roles.
# is_staff=False (default) == Participant (Student)
# is_staff=True == Privileged user (Judge, Manager, etc.) assigned to Groups.
class User(AbstractUser):
    pass

# --- 2. User Profile Model ---
# Stores extra, flexible information about a user.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Student-specific fields
    student_roll_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    
    # General & Professional fields
    about = models.TextField(blank=True, null=True)
    highlight = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="General skills: e.g., Design, Development, Management")
    technical_skillset = models.TextField(blank=True, null=True, help_text="Specifics: e.g., Python, Django, React")
    social_links = models.JSONField(default=dict, blank=True)
    professional_role = models.CharField(max_length=100, blank=True, null=True, help_text="For judges/mentors")
    organization_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# --- 3. Registration Code Model ---
# Used to gate participant sign-ups.
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

# --- 4. Event Registration Model ---
# Explicitly links a participant to an event they have registered for.
class EventRegistration(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                    related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, 
                              related_name="registrations") # Changed related_name for clarity
    
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('participant', 'event')

    def __str__(self):
        return f"{self.participant.username} registered for {self.event.event_name}"

# --- 5. Registration Log Model ---
# Audits all sign-up attempts for security and monitoring.
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
