from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import RegistrationCode, User, UserProfile, EventRegistration, ParticipantRegistrationLog
from .forms import ParticipantRegistrationForm

# --- Participant Registration View ---
def register_participant_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect logged-in users away

    if request.method == 'POST':
        form = ParticipantRegistrationForm(request.POST)
        
        ip_address = request.META.get('REMOTE_ADDR')
        email = request.POST.get('email', '').strip()
        code_str = request.POST.get('registration_code', '').strip()

        if form.is_valid():
            try:
                with transaction.atomic():
                    code = RegistrationCode.objects.select_for_update().get(code=code_str)

                    # 1. Validate the Code
                    if not code.is_active: raise ValueError("This code is not active.")
                    if code.expires_at and code.expires_at < timezone.now(): raise ValueError("This code has expired.")
                    if code.uses_count >= code.max_uses: raise ValueError("This code has reached its maximum uses.")

                    # 2. Create the User & Profile
                    user = User.objects.create_user(
                        username=form.cleaned_data['email'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        is_staff=False,
                        is_active=False # Recommended: Keep false until email is verified
                    )
                    
                    UserProfile.objects.create(
                        user=user,
                        student_roll_number=form.cleaned_data.get('student_roll_number'),
                        branch=form.cleaned_data.get('branch'),
                        year_of_study=form.cleaned_data.get('year_of_study')
                    )

                    # 3. Update the Code Usage
                    code.uses_count += 1
                    code.save()

                    # 4. Link User to Event if code is event-specific
                    if code.event:
                        EventRegistration.objects.create(participant=user, event=code.event)

                    # 5. Log Success & Send Email (Email sending logic needs setup)
                    ParticipantRegistrationLog.objects.create(
                        email_attempt=email, code_used=code_str, ip_address=ip_address, 
                        status='success', reason='Registration successful'
                    )
                    
                    messages.success(request, 'Registration successful! Please check your email to activate your account.')
                    return redirect('login')

            except RegistrationCode.DoesNotExist:
                messages.error(request, 'Invalid registration code.')
                ParticipantRegistrationLog.objects.create(email_attempt=email, code_used=code_str, ip_address=ip_address, status='fail', reason='Code does not exist')
            except ValueError as e:
                messages.error(request, str(e))
                ParticipantRegistrationLog.objects.create(email_attempt=email, code_used=code_str, ip_address=ip_address, status='fail', reason=str(e))
            except Exception as e:
                messages.error(request, 'An unexpected error occurred. Please check the form.')
                ParticipantRegistrationLog.objects.create(email_attempt=email, code_used=code_str, ip_address=ip_address, status='fail', reason=f"Form Error: {e}")
    else:
        form = ParticipantRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

# --- Login and Logout Views ---
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

# --- Dashboard Redirect View ---
@login_required
def dashboard_redirect_view(request):
    if request.user.is_staff:
        return redirect('event_manager_dashboard')
    else:
        return redirect('participant_dashboard')

# --- Participant Dashboard View ---
@login_required
def participant_dashboard_view(request):
    if request.user.is_staff:
        return redirect('event_manager_dashboard') # Prevent staff from accessing this

    my_registrations = EventRegistration.objects.filter(participant=request.user).select_related('event')
    context = {'my_registrations': my_registrations}
    return render(request, 'accounts/participant_dashboard.html', context)
