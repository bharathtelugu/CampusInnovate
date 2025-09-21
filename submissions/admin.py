from django.contrib import admin
from .models import Submission, Judging

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'team', 'problem_statement', 'submitted_at')
    list_filter = ('team__event',)
    search_fields = ('project_title', 'team__team_name')

class JudgingAdmin(admin.ModelAdmin):
    list_display = ('submission', 'judge', 'score')
    list_filter = ('submission__team__event', 'judge')
    search_fields = ('submission__project_title', 'judge__username')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Judging, JudgingAdmin)