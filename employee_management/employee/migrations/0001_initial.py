# Generated by Django 4.2 on 2024-11-12 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(max_length=10, unique=True)),
                ('subject', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('open', 'Open'), ('pending', 'Pending'), ('resolved', 'Resolved'), ('closed', 'Closed'), ('waiting_on_customer', 'Waiting on Customer'), ('initial_response', 'Initial Response')], max_length=50)),
                ('group', models.CharField(choices=[('Linux', 'Linux'), ('Windows', 'Windows/Azure'), ('AWS', 'Network/AWS'), ('LEVELONE', 'Level One'), ('OCI', 'OCI')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_at', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True)),
                ('assigned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigner_tickets', to=settings.AUTH_USER_MODEL)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tickets', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('1', 'Level 1')], max_length=10)),
                ('skill', models.CharField(choices=[('Linux', 'Linux'), ('Windows', 'Windows/Azure'), ('AWS', 'Network/AWS'), ('LEVELONE', 'Level One'), ('OCI', 'OCI')], max_length=20)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_on_break', models.BooleanField(default=False)),
                ('promoted_to_admin', models.BooleanField(default=False)),
                ('total_time', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('on_break', 'On Break'), ('offline', 'Offline')], default='offline', max_length=20)),
                ('login_time', models.DateTimeField(blank=True, null=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]