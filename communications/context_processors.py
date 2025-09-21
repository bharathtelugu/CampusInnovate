from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': count}
    return {}

**Now, register this in your `campusinnovate/settings.py`:**
```python
# campusinnovate/settings.py

TEMPLATES = [
    {
        # ... other settings ...
        'OPTIONS': {
            'context_processors': [
                # ... default processors ...
                'communications.context_processors.unread_notifications_count', # ADD THIS LINE
            ],
        },
    },
]

#### Step 2: Update Your `base.html` Template

Now you can use the `unread_notifications_count` variable in any template. Let's add it to your main navigation.

**Modify `templates/base.html`:**
```html
{# Find the part of your nav where user links are #}
{% if user.is_authenticated %}
    <a href="{% url 'notification-list' %}" class="relative">
        <span>Notifications</span>
        {% if unread_notifications_count > 0 %}
            <span class="absolute top-0 right-0 -mt-1 -mr-2 px-2 py-1 text-xs font-bold text-white bg-red-500 rounded-full">
                {{ unread_notifications_count }}
            </span>
        {% endif %}
    </a>
    <a href="{% url 'dashboard' %}">Dashboard</a>
    <a href="{% url 'logout' %}">Log Out</a>
{% endif %}

#### Step 3: Display Announcements on the Event Detail Page

Let's show event-specific announcements where they are most relevant.

**Modify `templates/events/event_detail.html`:**
```html
{# Add this section, for example, right below the "About This Event" section #}

<!-- Announcements -->
{% if event.announcements.all %}
    <h2 class="text-3xl font-bold mt-8 mb-4 text-yellow-600">Announcements</h2>
    <div class="space-y-4">
        {% for announcement in event.announcements.all %}
            <div class="border-l-4 border-yellow-400 bg-yellow-50 p-4 rounded-r-lg">
                <h3 class="text-xl font-semibold text-yellow-800">{{ announcement.title }}</h3>
                <p class="text-sm text-gray-500 mb-2">{{ announcement.created_at|date:"F d, Y, P" }}</p>
                <p class="text-yellow-700">{{ announcement.message|linebreaks }}</p>
            </div>
        {% endfor %}
    </div>
{% endif %}

{# ... rest of your event detail page ... #}

#### Step 4: Make Announcements Easy to Create for Staff

The best way for staff to create announcements is directly from the event's admin page.

**Modify `events/admin.py`:**
```python
from django.contrib import admin
from .models import Event # ... and your other event models ...
from communications.models import Announcement # IMPORT ANNOUNCEMENT

# Define an inline for Announcements
class AnnouncementInline(admin.TabularInline):
    model = Announcement
    extra = 1 # Show one blank form
    fields = ('title', 'message')

# Add the inline to your EventAdmin
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # ... all your other settings and inlines ...
    inlines = [
        # ... all your other inlines (ProblemStatementInline, etc.) ...
        AnnouncementInline, # ADD THIS LINE
    ]

#### Step 5: **(CRUCIAL)** Trigger Notifications from Other Apps

This is the final piece. We need to create `Notification` objects when important things happen. For example, when a user is invited to a team.

**Modify `teams/views.py` (or wherever your team logic is):**
```python
# This is a hypothetical view for sending a team invite
# You would add this logic to your actual team management view

from django.shortcuts import redirect
from django.urls import reverse
from communications.models import Notification # IMPORT NOTIFICATION
from .models import Team, TeamInvitation, User # and other models...

def send_team_invite_view(request, team_id):
    team = Team.objects.get(id=team_id)
    invited_email = request.POST.get('email')
    
    try:
        invited_user = User.objects.get(email=invited_email)

        # 1. Create the invitation object (your existing logic)
        invitation = TeamInvitation.objects.create(team=team, invited_email=invited_email)

        # 2. **CREATE THE NOTIFICATION**
        Notification.objects.create(
            user=invited_user,
            message=f"You have been invited to join the team '{team.team_name}' for the event '{team.event.event_name}'.",
            link=reverse('team-dashboard') # A hypothetical URL for the team page
        )
        
        # ... redirect with success message ...
    
    except User.DoesNotExist:
        # ... handle case where user doesn't exist ...
        pass
    
    return redirect('some-page')

Your `communications` app is now fully implemented and integrated. It provides a robust system for keeping your users updated on both an individual and event-wide level.