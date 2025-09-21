from django.urls import path
from . import views

urlpatterns = [
    # URL for participants to submit/edit their project for an event
    # e.g., /submissions/event/1/submit/
    path('event/<int:event_id>/submit/', views.submission_create_edit_view, name='submission_create_edit'),
    
    # URL for the judges' dashboard for a specific event
    # e.g., /submissions/judging/event/1/
    path('judging/event/<int:event_id>/', views.judging_dashboard_view, name='judging_dashboard'),
    
    # URL for a judge to score a specific submission
    # e.g., /submissions/judging/score/45/
    path('judging/score/<int:submission_id>/', views.submission_score_view, name='submission_score'),
]

