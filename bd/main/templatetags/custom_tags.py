from django import template

register = template.Library()

@register.simple_tag
def pluralize_type(type, total):
    if not type.endswith('s') and total > 1:
        return type + 's'
    return type
