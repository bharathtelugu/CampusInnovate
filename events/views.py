from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event, EventStaff

# --- Public-Facing Views ---

class EventListView(ListView):
    """
    Displays a list of all published events. This serves as the homepage.
    """
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    # We only want to show events that are ready for the public
    def get_queryset(self):
        return Event.objects.filter(status='published').order_by('-event_start').select_related('media')

class EventDetailView(DetailView):
    """
    Displays the full details for a single event.
    """
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

# --- Staff-Only Dashboard View ---

def is_staff_user(user):
    """A simple test function for the decorator."""
    return user.is_staff

@login_required
@user_passes_test(is_staff_user) # Protects the view, only staff can access
def event_manager_dashboard_view(request):
    """
    Serves as the main dashboard for all staff roles.
    It shows events the user is specifically assigned to.
    """
    managed_events_qs = EventStaff.objects.filter(user=request.user).select_related('event')
    
    context = {
        'managed_events': managed_events_qs,
    }
    return render(request, 'events/event_manager_dashboard.html', context)
