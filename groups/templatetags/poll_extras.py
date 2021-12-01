from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})
