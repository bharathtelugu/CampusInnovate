from django.db import models
from django.conf import settings
from events.models import Event
import uuid

def generate_unique_code():
    """Generates a unique 6-character uppercase alphanumeric code."""
    return str(uuid.uuid4().hex[:6].upper())

class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=100)
    team_code = models.CharField(max_length=20, unique=True, default=generate_unique_code, help_text="Unique code for invites")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='led_teams')
    max_size = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # The 'members' relationship is defined via a reverse relation from the TeamMember model

    class Meta:
        # A team name should be unique *within* a specific event
        unique_together = ('event', 'team_name')

    def __str__(self):
        return f"{self.team_name} ({self.event.event_name})"

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only be on one team per event
        unique_together = ('team', 'participant')

    def __str__(self):
        return f"{self.participant.username} in {self.team.team_name}"
