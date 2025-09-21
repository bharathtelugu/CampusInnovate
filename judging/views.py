from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from .models import Submission, Judging
from events.models import Event, EventStaff
from .forms import JudgingForm

def is_judge_for_event(user, event):
    """
    Checks if a user is assigned as a 'judge' for a specific event.
    """
    return EventStaff.objects.filter(user=user, event=event, role__iexact='judge').exists()

@login_required
def judging_dashboard_view(request, event_id):
    """
    Displays a dashboard for a judge listing all submissions for a specific event.
    """
    event = get_object_or_404(Event, pk=event_id)

    # Security Check: Ensure the logged-in user is actually a judge for this event.
    if not is_judge_for_event(request.user, event):
        messages.error(request, "You are not authorized to judge this event.")
        return redirect('event_manager_dashboard')

    # Get all submissions for the event
    submissions = Submission.objects.filter(team__event=event)
    
    # Get scores the current judge has already given for this event's submissions
    my_scores = Judging.objects.filter(judge=request.user, submission__in=submissions).values_list('submission_id', flat=True)

    context = {
        'event': event,
        'submissions': submissions,
        'my_scores': list(my_scores), # Pass the list of scored submission IDs to the template
    }
    return render(request, 'submissions/judging_dashboard.html', context)

@login_required
def submission_score_view(request, submission_id):
    """
    Allows a judge to view a submission's details and submit or edit a score.
    """
    submission = get_object_or_404(Submission, pk=submission_id)
    event = submission.team.event

    # Security Check: Ensure the user is a judge for this event.
    if not is_judge_for_event(request.user, event):
        messages.error(request, "You are not authorized to score this submission.")
        return redirect('event_manager_dashboard')
        
    # Check if this judge has already scored this submission
    judging_instance, created = Judging.objects.get_or_create(
        judge=request.user,
        submission=submission
    )

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
