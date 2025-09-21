from django import forms
from .models import Submission, Judging

class SubmissionForm(forms.ModelForm):
    """
    A form for participants (team leaders) to create or update their project submission.
    """
    class Meta:
        model = Submission
        fields = [
            'project_title', 
            'project_description', 
            'repo_link', 
            'demo_link', 
            'image_upload',
            'problem_statement',
        ]
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md'}),
            'project_description': forms.Textarea(attrs={'rows': 5, 'class': 'w-full p-2 border rounded-md'}),
            'repo_link': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-md'}),
            'demo_link': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-md'}),
            'image_upload': forms.FileInput(attrs={'class': 'w-full p-2 border rounded-md'}),
            'problem_statement': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
        }
        labels = {
            'repo_link': 'Repository Link (e.g., GitHub)',
            'demo_link': 'Demo Video Link (e.g., YouTube)',
            'image_upload': 'Upload an Image (Poster, Screenshot)',
        }

    def __init__(self, *args, **kwargs):
        # We need to pass the event to the form to dynamically filter the problem statements
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        if event:
            self.fields['problem_statement'].queryset = event.problem_statements.all()
            self.fields['problem_statement'].empty_label = "Select a Problem Statement"


class JudgingForm(forms.ModelForm):
    """
    A form for a judge to submit their score and feedback for a submission.
    """
    score = forms.FloatField(
        min_value=0, 
        max_value=100, 
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md'}),
        help_text="Enter a score between 0 and 100."
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'w-full p-2 border rounded-md'}),
        required=False,
        help_text="Provide constructive feedback for the team (optional)."
    )

    class Meta:
        model = Judging
        fields = ['score', 'feedback']

