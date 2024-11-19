# employee/templatetags/custom_filters.py

from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def mod(value, arg):
    """Returns the remainder of value divided by arg."""
    return value % arg


@register.filter
def format_timedelta(value):
    if isinstance(value, timedelta):
        # Get total seconds from the timedelta
        total_seconds = int(value.total_seconds())

        # Calculate hours, minutes, and seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Format as hh:mm:ss
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    return value