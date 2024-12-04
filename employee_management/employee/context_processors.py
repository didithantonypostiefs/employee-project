from .models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
    else:
        notifications = []

    return {
        'notifications': notifications
    }
