from django.contrib import admin
from .models import Team, TeamMember

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    readonly_fields = ('joined_at',)
    autocomplete_fields = ['participant']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'event', 'leader', 'created_at')
    list_filter = ('event',)
    search_fields = ('team_name', 'leader__username')
    inlines = [TeamMemberInline]
    autocomplete_fields = ['leader']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('participant', 'team', 'joined_at')
    list_filter = ('team__event',)
    search_fields = ('participant__username', 'team__team_name')
    autocomplete_fields = ['participant', 'team']
