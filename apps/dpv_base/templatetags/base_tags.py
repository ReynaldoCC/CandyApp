from django import template
from django.apps import apps as all_apps
from django.template.defaultfilters import stringfilter
from django.utils.safestring import SafeData, mark_safe
from locales_viv import settings

register = template.Library()

@register.simple_tag
def local_apps():
    local_apps = []
    if all_apps.get_app_configs:
        for app in all_apps.get_app_configs():
            if hasattr(app, 'owned') and app.active:
                local_apps.append(app)
    return local_apps

@register.simple_tag
def menuable_apps():
    menuable_apps = []
    if all_apps.get_app_configs:
        for app in all_apps.get_app_configs():
            if hasattr(app, 'owned') and app.active:
                if hasattr(app, 'menuable') and app.menuable:
                    if hasattr(app, 'model_data'):
                        if len(app.model_data) == 1:
                            setattr(app, 'count_data', app.get_model(app.model_data[0]).objects.all().count())
                        else:
                            setattr(app, 'count_data', all_apps.get_model(app.model_data[0], app.model_data[1]).objects.all().count())
                    menuable_apps.append(app)
    return menuable_apps

@register.simple_tag()
def exist_url(url=None):
    if not url:
        return False
    # for urlpat in settings.BULK_URLS:
    #
    #     if url in urlpat.name:
    #         return True
    return settings.BULK_URLS

@register.simple_tag()
def ative_url(url=None):
    if not url:
        return False
    for urlpath in settings.BULK_URLS:
        pass

@register.filter
@stringfilter
def split(value, arg):
    if not value:
        return
    safe = isinstance(value, SafeData)
    value = value.split(arg)
    if safe:
        return mark_safe(value)
    return value

@register.filter
def restof( value, arg):
    '''
    Divides the value; the argument is the divisor and it is ok return rest of division
    Returns empty string if some error
    '''
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value % arg
    except:
        pass
    return ''


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
    if value is None:
        value = 0
    return value


@register.filter
def tosub(value, arg):
    '''
    Sub this values and args if is posibile
    Returns empty string if some error
    '''
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value - arg
    except:
        pass
    return value
