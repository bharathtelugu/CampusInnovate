from django.contrib import admin
from .models import Submission, Judging

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'team', 'problem_statement', 'submitted_at')
    list_filter = ('team__event',) # Allows filtering by the event the team belongs to
    search_fields = ('project_title', 'team__team_name')
    readonly_fields = ('submitted_at', 'last_updated_at')
    autocomplete_fields = ['team', 'problem_statement']

@admin.register(Judging)
class JudgingAdmin(admin.ModelAdmin):
    list_display = ('submission', 'judge', 'score')
    list_filter = ('submission__team__event', 'judge')
    search_fields = ('submission__project_title', 'judge__username')
    autocomplete_fields = ['submission', 'judge']
