from django.urls import path
from . import views

urlpatterns = [
    # URL to create a new team for a specific event
    # e.g., /teams/event/1/create/
    path('event/<int:event_id>/create/', views.team_create_view, name='team_create'),
    
    # URL to join a team for a specific event
    # e.g., /teams/event/1/join/
    path('event/<int:event_id>/join/', views.team_join_view, name='team_join'),

    # URL for the main team dashboard/details page
    # e.g., /teams/45/
    path('<int:team_id>/', views.team_detail_view, name='team_detail'),

    # URL for a member to leave a team
    # e.g., /teams/45/leave/
    path('<int:team_id>/leave/', views.team_leave_view, name='team_leave'),
]
