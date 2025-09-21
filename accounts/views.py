from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone
from .models import RegistrationCode, User, UserProfile, EventRegistration, ParticipantRegistrationLog
from .forms import ParticipantRegistrationForm # You will need to create this form
from django.contrib import messages
# You'll also need to import your email-sending functions

def register_participant_view(request):
    if request.method == 'POST':
        form = ParticipantRegistrationForm(request.POST)
        
        # Get IP address for logging
        ip_address = request.META.get('REMOTE_ADDR')
        email = request.POST.get('email', '').strip()
        code_str = request.POST.get('registration_code', '').strip()

        if form.is_valid():
            try:
                # --- This is the critical, secure way to handle a code ---
                with transaction.atomic():
                    # Find the code and lock the database row for update
                    code = RegistrationCode.objects.select_for_update().get(code=code_str)

                    # --- 1. Validate the Code ---
                    if not code.is_active:
                        raise ValueError("This code is not active.")
                    if code.expires_at and code.expires_at < timezone.now():
                        raise ValueError("This code is expired.")
                    if code.uses_count >= code.max_uses:
                        raise ValueError("This code has reached its maximum uses.")

                    # --- 2. Create the User & Profile ---
                    user = form.save(commit=False)
                    user.is_staff = False # This is a Participant
                    user.is_active = False # (Recommended) Keep false until email verified
                    user.save()
                    
                    # Create the profile (assuming your form has profile fields)
                    UserProfile.objects.create(
                        user=user,
                        student_roll_number=form.cleaned_data.get('student_roll_number'),
                        branch=form.cleaned_data.get('branch'),
                        year_of_study=form.cleaned_data.get('year_of_study')
                    )

                    # --- 3. Update the Code Usage (Atomic) ---
                    code.uses_count += 1
                    code.save()

                    # --- 4. Register User for the Event (if code is event-specific) ---
                    if code.event:
                        EventRegistration.objects.create(
                            participant=user,
                            event=code.event,
                            status='registered'
                        )

                    # --- 5. Log Success & Send Email ---
                    ParticipantRegistrationLog.objects.create(
                        email_attempt=email, code_used=code_str, ip_address=ip_address, 
                        status='success', reason='Registration successful'
                    )
                    
                    # send_activation_email(user) # Your function to send email

                    messages.success(request, 'Registration successful! Please check your email to activate your account.')
                    return redirect('login') # Redirect to login page

            except RegistrationCode.DoesNotExist:
                messages.error(request, 'Invalid registration code.')
                ParticipantRegistrationLog.objects.create(
                    email_attempt=email, code_used=code_str, ip_address=ip_address, 
                    status='fail', reason='Code does not exist'
                )
            except ValueError as e:
                messages.error(request, str(e)) # Show the specific error (e.g., "Code expired")
                ParticipantRegistrationLog.objects.create(
                    email_attempt=email, code_used=code_str, ip_address=ip_address, 
                    status='fail', reason=str(e)
                )
            # Handle other form errors (e.g., email already exists)
            except Exception as e:
                messages.error(request, f'An unexpected error occurred. {e}')
                ParticipantRegistrationLog.objects.create(
                    email_attempt=email, code_used=code_str, ip_address=ip_address, 
                    status='fail', reason=str(e)
                )

    else:
        form = ParticipantRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})