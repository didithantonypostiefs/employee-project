# Generated by Django 4.2 on 2024-11-13 05:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employeeprofile_break_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeprofile',
            name='break_duration',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='break_start_time',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='total_work_time',
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField()),
                ('logout_time', models.DateTimeField()),
                ('break_duration', models.DurationField(default=datetime.timedelta)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='employee.employeeprofile')),
            ],
        ),
    ]