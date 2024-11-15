# employee/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def mod(value, arg):
    """Returns the remainder of value divided by arg."""
    return value % arg
