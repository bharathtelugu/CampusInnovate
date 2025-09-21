from django.contrib import admin
from django.urls import path, include
from events.views import EventListView # Import the new EventListView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Make the Event List the new homepage
    path('', EventListView.as_view(), name='home'), 
    
    # Account URLs (login, register, etc.)
    path('accounts/', include('accounts.urls')),
    
    # Event Detail URLs
    path('events/', include('events.urls')),

    # Judging URLs
    path('judging/', include('submissions.urls')),
    
    # ... any other app URLs ...
]
# This is required to serve media files (like submission images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)