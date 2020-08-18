from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def valuetoint(value):
    """
    Return the value converted to int if posibile
    Returns empty string if some error
    """
    try:
        value = int(value)
        return value
    except Exception as e:
        print(e)
        if not value:
            return 0
    return value


@register.filter
def is_list(value):

    return isinstance(value, list)


@register.filter
def is_queryset(value):
    return isinstance(value, QuerySet)
