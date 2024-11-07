from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from .models import EmployeeProfile
from django.shortcuts import redirect
from datetime import timedelta,datetime

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile_cache_key = f"profile_{request.user.id}"
            profile = cache.get(profile_cache_key)

            if not profile:
                # Use select_related to optimize query
                profile = EmployeeProfile.objects.select_related('user').get(user=request.user)
                cache.set(profile_cache_key, profile, timeout=60*5)  # Cache for 5 minutes

            updated = False

            # Check if the user is on a break and update the is_active status accordingly
            if profile.is_on_break:
                if profile.is_active:  # Only update if there's a change
                    profile.is_active = False
                    updated = True
            else:
                if not profile.is_active:  # Only update if there's a change
                    profile.is_active = True
                    updated = True

            # Update last_active timestamp only if more than 60 seconds have passed
            if (timezone.now() - profile.last_active).seconds > 60:
                profile.last_active = timezone.now()
                updated = True

            # Save profile only if changes were made
            if updated:
                profile.save()
                cache.set(profile_cache_key, profile, timeout=60*5)  # Update the cache

        # Proceed with the rest of the middleware stack
        response = self.get_response(request)
        return response


# middleware.py


