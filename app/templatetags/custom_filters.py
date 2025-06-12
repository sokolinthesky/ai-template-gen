# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def sort_items_by_title(items):
    return sorted(items, key=lambda i: i.title.lower())
