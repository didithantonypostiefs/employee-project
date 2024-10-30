# signals.py
from django.contrib.auth.signals import user_logged_out,user_logged_in
from django.dispatch import receiver
from .models import EmployeeProfile
from django.contrib.auth.models import User

@receiver(user_logged_out)
def set_inactive(sender, request, user, **kwargs):
    try:
        profile = EmployeeProfile.objects.select_related('user').get(user=user)
        profile.is_active = False
        profile.save()
    except EmployeeProfile.DoesNotExist:
        # Handle cases where the user does not have an EmployeeProfile
        pass




logged_in_users = set()

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    logged_in_users.add(user)

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    logged_in_users.discard(user)

