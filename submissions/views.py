from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Submission, Judging
from events.models import Event, EventStaff
from teams.models import Team 
from .forms import SubmissionForm, JudgingForm

# --- Participant Views ---

@login_required
def submission_create_edit_view(request, event_id):
    """
    Allows a team leader to create or edit their submission for a specific event.
    """
    event = get_object_or_404(Event, pk=event_id)
    
    # Security Check 1: Find the user's team for this event.
    try:
        team = Team.objects.get(event=event, members=request.user)
    except Team.DoesNotExist:
        messages.error(request, "You are not part of a team for this event.")
        return redirect('event-detail', pk=event_id)

    # Security Check 2: Only the team leader can submit or edit.
    if team.leader != request.user:
        messages.error(request, "Only the team leader can create or edit the submission.")
        return redirect('participant_dashboard')
        
    # Get existing submission or None if it doesn't exist
    submission_instance = Submission.objects.filter(team=team).first()

    if request.method == 'POST':
        # Pass the event to the form to filter problem statements
        form = SubmissionForm(request.POST, request.FILES, instance=submission_instance, event=event)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.team = team 
            submission.save()
            messages.success(request, "Your project submission has been saved successfully!")
            return redirect('participant_dashboard')
    else:
        form = SubmissionForm(instance=submission_instance, event=event)

    context = {
        'form': form,
        'event': event,
        'team': team,
        'submission': submission_instance,
    }
    return render(request, 'submissions/submission_form.html', context)

# --- Judge Views ---

def is_judge_for_event(user, event):
    """Checks if a user is assigned as a 'judge' for a specific event."""
    return user.is_staff and EventStaff.objects.filter(user=user, event=event, role__iexact='judge').exists()

@login_required
def judging_dashboard_view(request, event_id):
    """Displays a dashboard for a judge listing all submissions for a specific event."""
    event = get_object_or_404(Event, pk=event_id)
    if not is_judge_for_event(request.user, event):
        messages.error(request, "You are not authorized to judge this event.")
        return redirect('event_manager_dashboard')

    submissions = Submission.objects.filter(team__event=event)
    my_scored_submissions = Judging.objects.filter(judge=request.user, submission__in=submissions).values_list('submission_id', flat=True)

    context = {
        'event': event,
        'submissions': submissions,
        'my_scored_submissions': list(my_scored_submissions),
    }
    return render(request, 'submissions/judging_dashboard.html', context)

@login_required
def submission_score_view(request, submission_id):
    """Allows a judge to view a submission's details and submit or edit a score."""
    submission = get_object_or_404(Submission, pk=submission_id)
    event = submission.team.event
    if not is_judge_for_event(request.user, event):
        messages.error(request, "You are not authorized to score this submission.")
        return redirect('event_manager_dashboard')
        
    judging_instance, created = Judging.objects.get_or_create(judge=request.user, submission=submission)

    if request.method == 'POST':
        form = JudgingForm(request.POST, instance=judging_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your score for '{submission.project_title}' has been saved.")
            return redirect('judging_dashboard', event_id=event.id)
    else:
        form = JudgingForm(instance=judging_instance)

    context = {
        'submission': submission,
        'form': form,
    }
    return render(request, 'submissions/judging_form.html', context)

