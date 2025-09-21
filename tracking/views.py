from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Feedback
from events.models import Event, EventRegistration
from .forms import FeedbackForm

@login_required
def submit_feedback_view(request, event_id):
    """
    Allows a participant to submit feedback for an event they were registered for.
    """
    event = get_object_or_404(Event, pk=event_id)

    # Security Check 1: User must have been registered for the event.
    if not EventRegistration.objects.filter(participant=request.user, event=event).exists():
        messages.error(request, "You can only provide feedback for events you were registered for.")
        return redirect('participant_dashboard')

    # Security Check 2: Event must be over.
    if event.event_end > timezone.now():
        messages.error(request, "You can only provide feedback after the event has concluded.")
        return redirect('participant_dashboard')

    # Security Check 3: User cannot submit feedback more than once.
    existing_feedback = Feedback.objects.filter(participant=request.user, event=event).first()
    if existing_feedback:
        messages.info(request, "You have already submitted feedback for this event.")
        return redirect('participant_dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.participant = request.user
            feedback.save()
            messages.success(request, f"Thank you for your feedback on '{event.event_name}'!")
            return redirect('participant_dashboard')
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'tracking/feedback_form.html', context)
