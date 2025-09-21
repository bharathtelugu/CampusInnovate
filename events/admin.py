from django.contrib import admin
from admin_charts.admin import AdminChartMixin
from admin_charts.charts import Chart
from .models import (
    Event, ProblemStatement, Schedule, SubSchedule, FAQ, 
    EventMedia, EventStaff, Eligibility, HowToParticipate, 
    CertificatesAndRewards, EventResource
)

# --- Define all your inlines first ---

class ProblemStatementInline(admin.TabularInline): # Tabular is a compact, row-based view
    model = ProblemStatement
    extra = 1 # How many new blank forms to show

class ScheduleInline(admin.StackedInline): # Stacked is a taller, form-like view
    model = Schedule
    extra = 1

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

class EventStaffInline(admin.TabularInline): # This implements "Assign organizers"
    model = EventStaff
    extra = 1

class EligibilityInline(admin.TabularInline):
    model = Eligibility
    extra = 1

class HowToParticipateInline(admin.StackedInline):
    model = HowToParticipate
    extra = 1
    
class EventResourceInline(admin.TabularInline):
    model = EventResource
    extra = 1

# --- Now, create the main EventAdmin ---

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_start', 'event_end', 'event_mode')
    list_filter = ('event_mode', 'event_start')
    search_fields = ('event_name', 'title')
    
    # This is where the magic happens!
    # All these models can now be edited from the Event page.
    inlines = [
        EventStaffInline,
        ProblemStatementInline,
        ScheduleInline,
        FAQInline,
        EligibilityInline,
        HowToParticipateInline,
        EventResourceInline,
        # You can also add EventMedia, CertificatesAndRewards, etc.
    ]

# We register SubSchedule separately since it's an inline of an inline
@admin.register(SubSchedule)
class SubScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'time_start', 'time_end', 'activity_description')
    list_filter = ('schedule__event',) # Lets you filter by event!


@admin.register(Event)
class EventAdmin(AdminChartMixin, admin.ModelAdmin): # Add AdminChartMixin
    list_display = ('event_name', 'event_start', 'event_end', 'event_mode')
    # ... (all your other settings and inlines) ...
    
    def get_admin_charts(self, request):
        # This chart shows participants per day for this event
        chart = Chart.bar(
            "Registrations per Day",
            "accounts.EventRegistration", # The model to chart
            "registered_at__date",        # Group by this date field
        )
        # Filter the chart to only show data for the *current* event
        chart.filter_by("event__id", request.resolver_match.kwargs["object_id"])
        return [chart]