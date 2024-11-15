from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import admin_required
from .forms import UserEditForm,EmployeeProfileForm,TicketForm
from .models import EmployeeProfile,Ticket,DailyActivity,SessionActivity
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Max
from django.contrib import auth, messages
from django.shortcuts import render, redirect,HttpResponse
from django.db import IntegrityError


def get_logged_in_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        if '_auth_user_id' in data:
            user_ids.append(data.get('_auth_user_id'))
    return User.objects.filter(id__in=user_ids, employeeprofile__is_active=True)


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return redirect('login')

User = get_user_model()


from .signals import logged_in_users
@login_required
def home(request):
    if request.user.is_authenticated:
        logged_in_users_list = list(logged_in_users)
        status_filter = ['open', 'pending', 'waiting_on_customer', 'initial_response']
        all_tickets = Ticket.objects.filter(
            assigned_to__in=logged_in_users_list,
            status__in=status_filter
        ).order_by('-created_at')
        tickets_by_user = {}
        for ticket in all_tickets:
            ticket.created_at_ist = timezone.localtime(ticket.created_at)
            user_id = ticket.assigned_to.id
            if user_id not in tickets_by_user:
                tickets_by_user[user_id] = {
                    'user': ticket.assigned_to,
                    'latest_ticket': ticket,
                    'assigned_by': ticket.assigned_by,
                    'older_tickets': []
                }
            else:
                tickets_by_user[user_id]['older_tickets'].append(ticket)
        tickets_by_user = list(tickets_by_user.values())
    else:
        tickets_by_user = []
    return render(request, 'homepage.html', {'tickets_by_user': tickets_by_user})


def register(request):
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                is_admin = form.cleaned_data['is_admin']
                if is_admin:
                    EmployeeProfile.objects.create(user=user, is_admin=True)
                else:
                    level = form.cleaned_data['level']
                    skill = form.cleaned_data['skill']
                    EmployeeProfile.objects.create(user=user, level=level, skill=skill, is_admin=False)
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')
            except IntegrityError as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeProfileForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            user_profile, created = EmployeeProfile.objects.get_or_create(user=user)
            user_profile.is_active = True
            user_profile.save()
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'index.html', {'form': {'non_field_errors': ['Invalid username or password.']}})
    return render(request, 'index.html')

def logout(request):
    if request.user.is_authenticated:
        user_profile = EmployeeProfile.objects.filter(user=request.user).first()
        if user_profile:
            user_profile.is_active = False
            user_profile.save()
        auth.logout(request)
        messages.success(request, "You have successfully logged out.")
    return redirect('login')



@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    employee_profile = EmployeeProfile.objects.get(user=user)
    context = {
        'user': user,
        'employee_profile': employee_profile,
        'is_on_break': employee_profile.is_on_break,
    }
    return render(request, 'view_profile.html', context)

@login_required
def edit_user(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            profile.skill = form.cleaned_data['skill']
            profile.save()
            return redirect('view_profile', user_id=request.user.id)
    else:
        initial_data = {'skill': profile.skill}
        form = UserEditForm(instance=request.user, initial=initial_data)
    return render(request, 'edit_user.html', {'form': form})

@login_required
def employee_list(request):
    employees=EmployeeProfile.objects.all()
    return render(request,'employee_list.html',{'employees':employees})

@admin_required
def important_function_view(request):
    return render(request, 'important_function.html')

@login_required
def promote_to_admin(request, user_id):
    if request.user.employeeprofile.is_admin:
        employee = EmployeeProfile.objects.get(user_id=user_id)
        employee.is_admin = True
        employee.promoted_to_admin = True
        employee.save()
        messages.success(request, 'User has been promoted to admin.')
    return redirect('employee_list')

@login_required
def depromote_admin(request, user_id):
    if request.user.employeeprofile.is_admin:
        employee = EmployeeProfile.objects.get(user_id=user_id)
        if employee.promoted_to_admin:
            employee.is_admin = False
            employee.promoted_to_admin = False
            employee.save()
            messages.success(request, 'User has been demoted from admin.')
        else:
            messages.error(request, 'Cannot demote registered admin.')
    return redirect('employee_list')

@login_required
def employees_by_level(request, level):
    logged_in_users = get_logged_in_users()
    employees = EmployeeProfile.objects.filter(level=level, user__in=logged_in_users, is_on_break=False)
    return render(request, 'employee_by_level&skill.html', {'employees': employees, 'filter_type': f'Level {level}'})

@login_required
def employees_by_skill(request, skill):
    logged_in_users = get_logged_in_users()
    employees = EmployeeProfile.objects.filter(skill=skill, user__in=logged_in_users, is_on_break=False)
    return render(request, 'employee_by_level&skill.html', {'employees': employees, 'filter_type': skill})

from django.utils import timezone
from django.contrib.sessions.models import Session

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.assigned_by = request.user
            ticket.assigned_at = timezone.now()
            ticket.save()
            return redirect('/')
    else:
        form = TicketForm()
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]
    logged_in_users = User.objects.filter(id__in=user_ids, is_active=True, employeeprofile__is_on_break=False)
    employees = logged_in_users.values('id', 'username', 'employeeprofile__skill')
    context = {
        'form': form,
        'employees': list(employees),
    }
    return render(request, 'create_ticket.html', context)

@login_required
def user_tickets(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tickets = Ticket.objects.filter(assigned_to=user)
    return render(request, 'view_tickets.html', {
        'tickets': tickets,
        'user': user,
    })

def view_tickets(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # Get tickets assigned to the user
    tickets = Ticket.objects.filter(assigned_to=user)
    return render(request, 'view_tickets.html', {'user': user, 'tickets': tickets})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user.is_superuser or request.user == ticket.created_by:
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('view_tickets',user_id=ticket.assigned_to.id)
        else:
            form = TicketForm(instance=ticket)
        return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})
    else:
        return HttpResponseForbidden("You are not allowed to edit this ticket.")

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user.employeeprofile.is_admin:
        if request.method == 'POST':
            ticket.delete()
            return redirect('view_tickets', user_id=ticket.assigned_to.id)
        return render(request, 'delete_ticket.html', {'ticket': ticket})
    else:
        return HttpResponseForbidden("You are not allowed to delete this ticket.")

@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.assigned_to != request.user:
        return render(request, 'homepage.html', {
            'error': "You are not authorized to close this ticket.",
            'ticket_id': ticket_id,
        })
    if request.method == 'POST':
        ticket.status = 'closed'
        ticket.save()
        return redirect('home')
    return redirect('home')

def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.assigned_to != request.user:
        return render(request, 'homepage.html', {
            'error': "You are not authorized to assign this ticket.",
            'ticket_id': ticket_id,
        })
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            new_assigned_user_id = request.POST.get('assigned_user')
            new_assigned_user = get_object_or_404(User, id=new_assigned_user_id)
            ticket.assigned_to = new_assigned_user
            ticket.assigned_by = request.user
            ticket.assigned_at = timezone.now()
            ticket.save()
            messages.success(request, "Ticket assigned successfully.")
            return redirect('view_tickets', user_id=request.user.id)

    else:
        form = TicketForm(instance=ticket)
    logged_in_users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    return render(request, 'assign_ticket.html', {
        'ticket': ticket,
        'form': form,
        'logged_in_users': logged_in_users
    })

from django.utils import timezone
@login_required
def add_employee(request):
    if not request.user.employeeprofile.is_admin:
        messages.error(request, "You do not have permission to add employees.")
        return redirect('home')
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            employee_profile = EmployeeProfile.objects.create(
                user=user,
                level='1',
                skill=form.cleaned_data['skill'],
                is_admin=form.cleaned_data['is_admin']
            )
            messages.success(request, "Employee added successfully!")
            return redirect('home')
    else:
        form = EmployeeProfileForm()
    return render(request, 'add_employee.html', {'form': form})


@login_required
def toggle_break_status(request):
    user_profile = request.user.employeeprofile
    user_profile.is_on_break = not user_profile.is_on_break  # Toggle break status
    user_profile.save()

    # Update the session activity for the current session
    today = timezone.now().date()
    try:
        current_session = SessionActivity.objects.filter(user=request.user, date=today, logout_time=None).latest(
            'login_time')

        if user_profile.is_on_break:
            # If the user is now on break, we record the time when the break starts
            current_session.break_start_time = timezone.now()  # Record the time when break starts
            current_session.save()
        else:
            # If the user is no longer on break, calculate the break duration
            break_duration = timezone.now() - current_session.break_start_time  # Time since break started
            current_session.break_duration += break_duration  # Add this break time to the session's break duration
            current_session.work_time = current_session.calculate_work_time()  # Recalculate work time based on the updated break duration
            current_session.save()

    except SessionActivity.DoesNotExist:
        pass  # No active session found, nothing to update

    return redirect('user_activity_view', user_id=request.user.id)


@login_required
def user_profile_view(request):
    user_profile = EmployeeProfile.objects.get(user=request.user)
    total_hours = user_profile.total_time.total_seconds() / 3600
    return render(request, 'profile.html', {'total_hours': total_hours})

def sidebar_view(request):
    skills = ['Windows', 'Linux', 'AWS', 'OCI', 'LEVELONE']
    return render(request, 'home_ticket.html', {'skills': skills})


@login_required
def toggle_break(request):
    user_profile = request.user.employeeprofile
    user_profile.is_on_break = not user_profile.is_on_break
    user_profile.save()
    return redirect('view_profile', user_id=request.user.id)



def employee_list_view(request):
    employees = EmployeeProfile.objects.all()
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in sessions:
        data = session.get_decoded()
        user_ids.append(data.get('_auth_user_id', None))
    logged_in_users = get_user_model().objects.filter(id__in=user_ids)
    return render(request, 'employee_list.html', {
        'employees': employees,
        'logged_in_users': logged_in_users,
        'filter_type': 'All Employees'
    })

from django.contrib.auth.models import User

def ticket_overview_view(request):
    users_with_tickets = User.objects.prefetch_related('ticket_set').filter(ticket__isnull=False)
    context = {
        'users_with_tickets': users_with_tickets,
    }
    return render(request, 'homepage.html', context)

def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours} hours, {minutes} minutes, {seconds} seconds"

@login_required
def daily_activity_view(request):
    selected_date = request.GET.get('date', None)
    if selected_date:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = timezone.now().date()

    # Get today's activities (one per user)
    activities = DailyActivity.objects.filter(date=selected_date).order_by('login_time')

    # Format total work time for each activity
    for activity in activities:
        activity.total_work_time_str = format_duration(activity.calculate_total_work_time())
        activity.total_break_time = format_duration(activity.calculate_total_break_time())

    return render(request, 'daily_activity.html', {'activities': activities,'selected_date': selected_date})




@login_required
def user_activity_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Get the selected date from the request (if none, default to today)
    selected_date = request.GET.get('date', None)
    if selected_date:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = timezone.now().date()

    # Fetch all sessions for the user on the selected date from SessionActivity
    activities = SessionActivity.objects.filter(user=user, date=selected_date).order_by('login_time')

    # Format the work time and break duration for each session
    for activity in activities:
        activity.work_time_str = format_duration(activity.work_time)
        activity.break_duration_str = format_duration(activity.break_duration)

    return render(request, 'user_activity.html', {
        'user': user,
        'activities': activities,
        'selected_date': selected_date
    })
