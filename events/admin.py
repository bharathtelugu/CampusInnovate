from django.contrib import admin
from .models import (
    Event, ProblemStatement, Schedule, SubSchedule, FAQ, 
    EventMedia, EventStaff, Eligibility, HowToParticipate, 
    CertificatesAndRewards, EventResource
)
# We import Announcement to inline it here for easy management
from communications.models import Announcement

# --- Inlines for the EventAdmin ---
# These allow managing all related data from the main Event page.

class EventMediaInline(admin.StackedInline):
    model = EventMedia

class ProblemStatementInline(admin.TabularInline):
    model = ProblemStatement
    extra = 1

class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 1

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

class EventStaffInline(admin.TabularInline):
    model = EventStaff
    extra = 1
    autocomplete_fields = ['user'] # Makes selecting users easier

class AnnouncementInline(admin.TabularInline):
    model = Announcement
    extra = 1
    fields = ('title', 'message')

class EligibilityInline(admin.StackedInline):
    model = Eligibility
    extra = 0

# --- Main Event Admin Configuration ---
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'status', 'event_start', 'event_end', 'event_mode')
    list_filter = ('status', 'event_mode', 'event_start')
    search_fields = ('event_name', 'title')
    
    # All related models are managed from this single page
    inlines = [
        EventMediaInline,
        EventStaffInline,
        ProblemStatementInline,
        ScheduleInline,
        AnnouncementInline,
        FAQInline,
        EligibilityInline,
    ]

# --- Other Admins (Optional but helpful) ---
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('event', 'day_number', 'date')
    list_filter = ('event',)

@admin.register(SubSchedule)
class SubScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'time_start', 'time_end', 'activity_description')
    list_filter = ('schedule__event',)
