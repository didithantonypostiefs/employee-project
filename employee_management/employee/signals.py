# signals.py
from django.contrib.auth.signals import user_logged_out,user_logged_in
from django.dispatch import receiver
from .models import EmployeeProfile
from django.contrib.auth.models import User

@receiver(user_logged_out)
def set_inactive(sender, request, user, **kwargs):
    profile = EmployeeProfile.objects.get(user=user)
    profile.is_active = False
    profile.save()







logged_in_users = set()

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    logged_in_users.add(user)

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    logged_in_users.discard(user)

