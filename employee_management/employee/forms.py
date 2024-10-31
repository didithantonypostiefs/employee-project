from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile
from .models import Ticket
from django.contrib.sessions.models import Session
from django.utils import timezone

# Only Level 1 remains
LEVEL_CHOICES = (
    ('1', 'Level 1'),
)

# Skills for Level 1 (or you can keep them as they are if not tied to levels)
SKILL_CHOICES = (
    ('Linux', 'Linux'),
    ('Windows', 'Windows/Azure'),
    ('AWS', 'Network/AWS'),
    ('LEVELONE', 'Level One'),
    ('OCI', 'OCI'),
)


class EmployeeProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    # Updated: Only Level 1
    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'form-control'}))

    # Keep relevant skills
    skill = forms.ChoiceField(choices=SKILL_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'form-control'}))

    is_admin = forms.BooleanField(required=False, label="Make this user an admin", widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        is_admin = cleaned_data.get('is_admin')
        level = cleaned_data.get('level')
        skill = cleaned_data.get('skill')

        # Skip validation for level and skill if the user is an admin
        if not is_admin:
            if not level:
                self.add_error('level', 'This field is required.')
            if not skill:
                self.add_error('skill', 'This field is required.')

        return cleaned_data


class UserEditForm(forms.ModelForm):
    skill = forms.ChoiceField(choices=SKILL_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class TicketForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.none(), required=False, label="Assign to")

    class Meta:
        model = Ticket
        fields = ['subject', 'status', 'group', 'assigned_to']
        widgets = {
            'subject': forms.Textarea(attrs={'rows': 4, 'maxlength': 300}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all active sessions
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

        # Get user ids from active sessions
        user_ids = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id', None)
            if user_id:
                user_ids.append(user_id)

        # Get users who are logged in, active, and not on break
        logged_in_users = User.objects.filter(id__in=user_ids, is_active=True, employeeprofile__is_on_break=False)
        self.fields['assigned_to'].queryset = logged_in_users


