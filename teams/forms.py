from django import forms
from .models import Team

class TeamCreateForm(forms.ModelForm):
    """
    Form for a participant to create a new team for an event.
    """
    class Meta:
        model = Team
        fields = ['team_name', 'max_size']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Enter your awesome team name'}),
            'max_size': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md', 'min': 2, 'max': 10}),
        }
        labels = {
            'team_name': 'Team Name',
            'max_size': 'Maximum Team Size (e.g., 5)',
        }

class TeamJoinForm(forms.Form):
    """
    Form for a participant to join an existing team using a team code.
    """
    team_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Enter the 6-digit team code'}),
        label="Team Invitation Code"
    )
