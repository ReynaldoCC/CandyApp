from django.template import Variable
from django import template

register = template.Library()

@register.filter(is_safe=False)
def filter(value, arg):
    values = []

    try:
        field, equal = arg.split(':')
    except:
        return values
    else:
        for i in range(0,len(value)):
            try:
                variable = str(Variable(field).resolve(value[i]))
            except:
                continue
            else:
                if variable == equal:
                    values.append(value[i])
    finally:
        return values

@register.filter(is_safe=False)
def filterinverted(value, arg):
    values = []

    try:
        field, equal = arg.split(':')
    except:
        return values
    else:
        for i in range(0,len(value)):
            try:
                variable = str(Variable(field).resolve(value[i]))
            except:
                continue
            else:
                if variable != equal:
                    values.append(value[i])
    finally:
        return values