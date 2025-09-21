from django.urls import path
from . import views

urlpatterns = [
    # The dashboard for a specific event's judging (e.g., /judging/event/1/)
    path('event/<int:event_id>/', views.judging_dashboard_view, name='judging_dashboard'),
    
    # The page to score a specific submission (e.g., /judging/score/45/)
    path('score/<int:submission_id>/', views.submission_score_view, name='submission_score'),
]
