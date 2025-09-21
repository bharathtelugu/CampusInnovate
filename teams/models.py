from django.db import models
from django.conf import settings
from events.models import Event  # Assuming events app is at the root

class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=100)
    team_code = models.CharField(max_length=20, unique=True, help_text="Unique code for invites")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='led_teams')
    max_size = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A team name should be unique *within* an event
        unique_together = ('event', 'team_name')

    def __str__(self):
        return f"{self.team_name} ({self.event.event_name})"

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('mentor', 'Mentor'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('removed', 'Removed'),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only be on one team per event
        unique_together = ('event', 'participant')
    
    def __str__(self):
        return f"{self.participant.username} in {self.team.team_name}"
    
    # Add a property to get the event directly for the unique_together constraint
    @property
    def event(self):
        return self.team.event

class TeamInvitation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    invited_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite to {self.invited_email} for {self.team.team_name}"