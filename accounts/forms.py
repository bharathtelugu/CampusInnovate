from django import forms
from .models import User
from django.core.exceptions import ValidationError

class ParticipantRegistrationForm(forms.ModelForm):
    # Fields for the User model
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'College Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True, label="Confirm Password")

    # Fields for the UserProfile model
    student_roll_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Roll Number'}))
    branch = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Branch (e.g., CSE)'}))
    year_of_study = forms.IntegerField(required=True, min_value=1, max_value=5, widget=forms.NumberInput(attrs={'placeholder': 'Year of Study'}))

    # Custom field for the code
    registration_code = forms.CharField(max_length=50, required=True, label="Registration Code", widget=forms.TextInput(attrs={'placeholder': 'Registration Code'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password'] # Base fields for the form

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        
        # Optional: Enforce a specific college email domain
        # Replace 'kvsrit.edu.in' with your actual college domain
        # if not email.endswith('@kvsrit.edu.in'):
        #     raise ValidationError("You must use a valid college email address.")
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return password_confirm
