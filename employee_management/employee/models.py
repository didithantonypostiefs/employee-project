from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

LEVEL_CHOICES = (
    ('1', 'Level 1'),
)

SKILL_CHOICES = (
    ('Linux', 'Linux'),
    ('Windows', 'Windows/Azure'),
    ('AWS', 'Network/AWS'),
    ('LEVELONE', 'Level One'),
    ('OCI', 'OCI'),
)

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    skill = models.CharField(max_length=20, choices=SKILL_CHOICES)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_on_break = models.BooleanField(default=False)
    promoted_to_admin = models.BooleanField(default=False)
    total_time = models.DurationField(default=timezone.timedelta)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('on_break', 'On Break'),
        ('offline', 'Offline')
    ], default='offline')
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)


class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,default='AUTO')
    subject = models.CharField(max_length=300)
    status = models.CharField(max_length=50, choices=[
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('waiting_on_customer', 'Waiting on Customer'),
        ('initial_response', 'Initial Response'),
    ])
    group = models.CharField(max_length=100, choices=[
        ('Linux', 'Linux'),
        ('Windows', 'Windows/Azure'),
        ('AWS', 'Network/AWS'),
        ('LEVELONE', 'Level One'),
        ('OCI', 'OCI'),
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_tickets')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tickets')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigner_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)  # Add this field to hold the ticket note

    class Meta:
        managed = False

    def __str__(self):
        return self.subject