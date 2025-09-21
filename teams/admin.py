from django.contrib import admin
from .models import Team, TeamMember, TeamInvitation

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'event', 'leader', 'created_at')
    list_filter = ('event',)
    search_fields = ('team_name', 'leader__username')

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('participant', 'team', 'role', 'status')
    list_filter = ('team__event', 'status', 'role')
    search_fields = ('participant__username', 'team__team_name')

admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TeamInvitation)