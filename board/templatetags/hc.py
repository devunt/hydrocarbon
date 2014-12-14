from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
def label_as_placeholder(field):
    field.field.widget.attrs.update({'placeholder': field.label})
    return field

@register.filter
@stringfilter
def split_first(value):
    return value.split()[0]
