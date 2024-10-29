# middleware.py
from django.utils import timezone
from .models import EmployeeProfile


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update the employee's active status and last activity timestamp
            profile = EmployeeProfile.objects.get(user=request.user)
            if profile.is_on_break:
                profile.is_active = False  # Not active when on break
            else:
                profile.is_active = True  # Active when not on break
            profile.last_active = timezone.now()
            profile.save()

        response = self.get_response(request)
        return response
