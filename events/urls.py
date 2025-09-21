from django.urls import path
from . import views

urlpatterns = [
    # URL for the staff dashboard
    path('dashboard/manager/', views.event_manager_dashboard_view, name='event_manager_dashboard'),

    # URL for the public event detail page (e.g., /events/1/)
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
]
