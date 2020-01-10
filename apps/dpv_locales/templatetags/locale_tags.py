from django import template


register = template.Library()


@register.filter
def valuetoint(value):
    '''
    Return the value converted to int if posibile
    Returns empty string if some error
    '''
    try:
        value = int(value)
        return value
    except:
        pass
    return value