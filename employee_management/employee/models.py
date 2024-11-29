from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
    total_time = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('on_break', 'On Break'),
        ('offline', 'Offline')
    ], default='offline')


class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    break_duration = models.DurationField(default=timezone.timedelta)
    total_work_time = models.DurationField(default=timezone.timedelta)


    def calculate_total_work_time(self):
        # Calculate total work time by summing all session times from SessionActivity for the user on this date
        sessions = SessionActivity.objects.filter(user=self.user, date=self.date)
        total_work_time = timezone.timedelta()
        for session in sessions:
            total_work_time += session.work_time
        return total_work_time

    def calculate_total_break_time(self):
        # Sum up break durations from all sessions for this user on the same date
        sessions = SessionActivity.objects.filter(user=self.user, date=self.date)
        total_break_time = timezone.timedelta()
        for session in sessions:
            total_break_time += session.break_duration
        return total_break_time

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class SessionActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    break_start_time = models.DateTimeField(null=True, blank=True)
    break_duration = models.DurationField(default=timezone.timedelta)
    work_time = models.DurationField(default=timezone.timedelta)  # Work time for this session

    def calculate_work_time(self):
        if self.login_time and self.logout_time:
            session_time = self.logout_time - self.login_time
            return session_time - self.break_duration
        return timezone.timedelta()  # Return 0 if the session is incomplete

    def __str__(self):
        return f"{self.user.username} - Session on {self.date}"


class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10, unique=True)
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
    assigned_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    work_start_time = models.DateTimeField(null=True, blank=True)  # When the user clicks start
    time_spent = models.DurationField(default=timezone.timedelta(0))
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False


    def start_work(self):
        self.work_start_time = timezone.now()
        self.save()

    def pause_work(self):
        """Pause the work timer and accumulate the time spent."""
        if self.work_start_time:
            time_diff = timezone.now() - self.work_start_time
            # Update time spent, ensuring to exclude any break time that was added to the session
            self.time_spent += time_diff
            self.work_start_time = None  # Pause the work
            self.save()

    def stop_work(self):
        # This can be used when the user finishes the ticket
        self.pause_work()  # Just pause work and leave the time_spent


    def __str__(self):
        return self.subject