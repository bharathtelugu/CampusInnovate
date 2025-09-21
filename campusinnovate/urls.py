from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.views import EventListView # Import the homepage view

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # App URLs
    # This includes all the URL patterns from each of our apps.
    path('accounts/', include('accounts.urls')),
    path('communications/', include('communications.urls')),
    path('events/', include('events.urls')),
    path('submissions/', include('submissions.urls')),
    path('teams/', include('teams.urls')),
    path('tracking/', include('tracking.urls')),

    # Homepage
    # The root URL of the site will show the list of all published events.
    path('', EventListView.as_view(), name='home'),
]

# This is a helper for serving user-uploaded media files (like submission images)
# during development. It should NOT be used in a production environment.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

