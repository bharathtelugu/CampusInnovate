from django import forms
from .models import Judging

class JudgingForm(forms.ModelForm):
    """
    A form for a judge to submit their score and feedback for a submission.
    """
    # We can add validation here, e.g., score between 1 and 100.
    score = forms.FloatField(
        min_value=0, 
        max_value=100, 
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md'})
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'w-full p-2 border rounded-md'}),
        required=False
    )

    class Meta:
        model = Judging
        fields = ['score', 'feedback']
