# signals.py
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import EmployeeProfile

@receiver(user_logged_out)
def set_inactive(sender, request, user, **kwargs):
    profile = EmployeeProfile.objects.get(user=user)
    profile.is_active = False
    profile.save()
