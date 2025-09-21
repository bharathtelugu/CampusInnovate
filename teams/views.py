from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Team, TeamMember
from events.models import Event, EventRegistration
from .forms import TeamCreateForm, TeamJoinForm

@login_required
def team_create_view(request, event_id):
    """Allows a registered participant to create a new team for an event."""
    event = get_object_or_404(Event, pk=event_id)

    # Security Check 1: User must be registered for the event.
    if not EventRegistration.objects.filter(participant=request.user, event=event).exists():
        messages.error(request, "You must be registered for this event to create a team.")
        return redirect('event-detail', pk=event_id)

    # Security Check 2: User cannot be in another team for this event.
    if TeamMember.objects.filter(participant=request.user, team__event=event).exists():
        messages.error(request, "You are already in a team for this event.")
        team_member = TeamMember.objects.get(participant=request.user, team__event=event)
        return redirect('team_detail', team_id=team_member.team.id)

    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    team = form.save(commit=False)
                    team.event = event
                    team.leader = request.user
                    team.save()

                    TeamMember.objects.create(team=team, participant=request.user)
                    
                    messages.success(request, f"Team '{team.team_name}' created successfully!")
                    return redirect('team_detail', team_id=team.id)
            except Exception as e:
                messages.error(request, f"A team with this name already exists for this event. Please choose another name.")
    else:
        form = TeamCreateForm()

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'teams/team_create.html', context)

@login_required
def team_detail_view(request, team_id):
    """Displays the dashboard for a specific team, for its members only."""
    team = get_object_or_404(Team.objects.prefetch_related('members__participant__profile'), pk=team_id)
    
    user_is_member = team.members.filter(participant=request.user).exists()
    if not user_is_member and not request.user.is_staff:
        messages.error(request, "You are not authorized to view this team page.")
        return redirect('participant_dashboard')

    context = {
        'team': team,
        'is_leader': team.leader == request.user,
    }
    return render(request, 'teams/team_detail.html', context)

@login_required
def team_join_view(request, event_id):
    """Allows a registered participant to join a team using a team code."""
    event = get_object_or_404(Event, pk=event_id)

    if not EventRegistration.objects.filter(participant=request.user, event=event).exists():
        messages.error(request, "You must be registered for this event to join a team.")
        return redirect('event-detail', pk=event_id)

    if TeamMember.objects.filter(participant=request.user, team__event=event).exists():
        messages.error(request, "You are already in a team for this event.")
        team_member = TeamMember.objects.get(participant=request.user, team__event=event)
        return redirect('team_detail', team_id=team_member.team.id)
    
    if request.method == 'POST':
        form = TeamJoinForm(request.POST)
        if form.is_valid():
            team_code = form.cleaned_data['team_code'].upper()
            try:
                with transaction.atomic():
                    team_to_join = Team.objects.select_for_update().get(team_code=team_code, event=event)
                    
                    if team_to_join.members.count() >= team_to_join.max_size:
                        messages.error(request, f"Cannot join. Team '{team_to_join.team_name}' is already full.")
                        return redirect('team_join', event_id=event.id)
                    
                    TeamMember.objects.create(team=team_to_join, participant=request.user)
                    messages.success(request, f"You have successfully joined team '{team_to_join.team_name}'!")
                    return redirect('team_detail', team_id=team_to_join.id)
            except Team.DoesNotExist:
                messages.error(request, "Invalid team code for this event. Please check the code and try again.")
    else:
        form = TeamJoinForm()

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'teams/team_join.html', context)

@login_required
def team_leave_view(request, team_id):
    """Allows a member to leave a team. If the leader leaves, the team is disbanded if they are the last member."""
    team = get_object_or_404(Team, pk=team_id)
    membership = get_object_or_404(TeamMember, team=team, participant=request.user)

    if request.method == 'POST':
        if team.leader == request.user:
            if team.members.count() > 1:
                messages.error(request, "As the team leader, you must transfer leadership or be the last member to leave.")
                return redirect('team_detail', team_id=team.id)
            else:
                team.delete()
                messages.success(request, "You have left the team, and the team has been disbanded.")
                return redirect('participant_dashboard')
        else:
            membership.delete()
            messages.success(request, f"You have left the team '{team.team_name}'.")
            return redirect('participant_dashboard')

    return render(request, 'teams/team_leave_confirm.html', {'team': team})
