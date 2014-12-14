from django import template


register = template.Library()

@register.filter
def label_as_placeholder(field):
    field.field.widget.attrs.update({'placeholder': field.label})
    return field
