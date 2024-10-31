from django.urls import path
from . import views

urlpatterns=[

    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('profile/<int:user_id>/',views.view_profile,name='view_profile'),
    path('edit_user/',views.edit_user,name='edit_user'),
    path('employee_list',views.employee_list,name='employee_list'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('important-function/',views.important_function_view,name='important_function'),
    path('promote_to_admin/<int:user_id>/',views.promote_to_admin,name='promote_to_admin'),
    path('depromote_admin/<int:user_id>/', views.depromote_admin, name='depromote_admin'),
    path('employees/level/<str:level>/',views.employees_by_level,name='employees_by_level'),
    path('employees/skill/<str:skill>/', views.employees_by_skill,name='employees_by_skill'),
    path('create_ticket/',views.create_ticket,name='create_ticket'),
    path('user_tickets/<int:user_id>/',views.user_tickets,name='user_tickets'),
    path('profile/<int:user_id>/tickets/', views.view_tickets, name='view_tickets'),
    path('ticket/edit/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('toggle-break/', views.toggle_break, name='toggle_break'),
    path('assign_ticket/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),

]