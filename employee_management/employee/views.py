from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import admin_required
from .forms import UserEditForm,EmployeeProfileForm,TicketForm
from .models import EmployeeProfile,Ticket
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Max
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib import auth, messages
from django.shortcuts import render, redirect,HttpResponse
from django.db import IntegrityError


def get_logged_in_users():
    # Get active sessions
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Extract user ids from the sessions
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        if '_auth_user_id' in data:
            user_ids.append(data.get('_auth_user_id'))

    # Fetch users whose profiles are marked as active
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
        # Get the list of logged-in users
        logged_in_users_list = list(logged_in_users)  # Convert to a list to use in queryset filter

        # Define the statuses that should be displayed
        status_filter = ['open', 'pending', 'waiting_on_customer', 'initial_response']

        # Filter tickets assigned to the logged-in users and exclude 'Resolved' and 'Closed' statuses
        all_tickets = Ticket.objects.filter(
            assigned_to__in=logged_in_users_list,
            status__in=status_filter  # Exclude 'Resolved' and 'Closed' statuses
        ).order_by('-created_at')

        # Prepare data for rendering
        tickets_by_user = {}
        for ticket in all_tickets:
            ticket.created_at_ist = timezone.localtime(ticket.created_at)
            user_id = ticket.assigned_to.id  # Grouping by the user assigned the ticket
            if user_id not in tickets_by_user:
                tickets_by_user[user_id] = {
                    'user': ticket.assigned_to,  # Reflect the user assigned the ticket
                    'latest_ticket': ticket,
                    'assigned_by': ticket.created_by,
                    'older_tickets': []
                }
            else:
                tickets_by_user[user_id]['older_tickets'].append(ticket)

        # Convert the dictionary to a list for rendering
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
        # Attempt to retrieve the user profile, but only if it exists
        user_profile = EmployeeProfile.objects.filter(user=request.user).first()

        if user_profile:
            # Set user profile to inactive if it exists
            user_profile.is_active = False
            user_profile.save()

        # Log out the user
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
            employee.promoted_to_admin = False  # Reset this field
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




@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.assigned_by = request.user
            ticket.save()
            return redirect('/')
    else:
        form = TicketForm()

    return render(request, 'create_ticket.html', {'form': form})


@login_required
def user_tickets(request, user_id):
    # Fetch tickets assigned to the user
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
                return redirect('view_tickets',user_id=ticket.created_by.id)
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
            return redirect('view_tickets', user_id=ticket.created_by.id)
        return render(request, 'delete_ticket.html', {'ticket': ticket})
    else:
        return HttpResponseForbidden("You are not allowed to delete this ticket.")


@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Check if the logged-in user is the user assigned to this ticket
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



@login_required
def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Check if the logged-in user is the assigned user for this ticket
    if ticket.assigned_to != request.user:
        return render(request, 'homepage.html', {
            'error': "You are not authorized to assign this ticket.",
            'ticket_id': ticket_id,
        })

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)  # Bind form to the ticket instance
        if form.is_valid():
            ticket = form.save(commit=False)
            new_assigned_user_id = request.POST.get('assigned_user')
            new_assigned_user = get_object_or_404(User, id=new_assigned_user_id)

            # Update the ticket's assigned user
            ticket.assigned_to = new_assigned_user
            ticket.assigned_by = request.user
            ticket.save()

            messages.success(request, "Ticket assigned successfully.")
            return redirect('view_tickets', user_id=request.user.id)  # Redirect to the user's tickets page

    else:
        form = TicketForm(instance=ticket)  # Pre-fill the form with the ticket data

    logged_in_users = User.objects.filter(is_active=True).exclude(id=request.user.id)

    return render(request, 'assign_ticket.html', {
        'ticket': ticket,
        'form': form,  # Pass the form to the template
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
    user_profile = EmployeeProfile.objects.get(user=request.user)

    if user_profile.status == 'active':
        user_profile.status = 'on_break'
        user_profile.break_start = timezone.now()
    elif user_profile.status == 'on_break':
        break_duration = timezone.now() - user_profile.break_start
        user_profile.total_time -= break_duration
        user_profile.status = 'active'

    user_profile.save()
    return redirect('home')



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

