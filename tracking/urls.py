from django.urls import path
from . import views

urlpatterns = [
    # URL for a participant to submit feedback for a specific event
    # e.g., /tracking/event/1/feedback/
    path('event/<int:event_id>/feedback/', views.submit_feedback_view, name='submit_feedback'),
]
