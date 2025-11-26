from django import template

register = template.Library()


@register.simple_tag
def pluralize_word(words, total):
    value = ""
    for word in words.split(" "):
        if not word.endswith('s') and total > 1:
            value += word + 's' + " "
        else:
            value += word + " "
    return value
