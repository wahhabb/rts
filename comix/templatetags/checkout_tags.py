from django import template

register = template.Library()


@register.inclusion_tag('cart/form_table_row.html' )
def form_table_row(form_field):
    return {'form_field': form_field}