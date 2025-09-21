from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    """
    Displays a list of notifications for the currently logged-in user.
    """
    model = Notification
    template_name = 'communications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 15 # Show 15 notifications per page

    def get_queryset(self):
        # Return notifications only for the current user
        return Notification.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # When the user visits the page, mark all their unread notifications as read.
        # This is a simple and effective approach.
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return super().get(request, *args, **kwargs)
