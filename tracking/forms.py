from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    """
    A form for participants to submit feedback for an event.
    """
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={'class': 'flex gap-x-4'}
            ),
            'comments': forms.Textarea(
                attrs={
                    'class': 'w-full p-2 border rounded-md h-32',
                    'placeholder': 'Tell us about your experience! What went well? What could be improved?'
                }
            ),
        }
        labels = {
            'rating': 'Overall Rating (1=Poor, 5=Excellent)',
            'comments': 'Your Comments',
        }
