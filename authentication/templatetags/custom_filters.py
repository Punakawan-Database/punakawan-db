import locale

from django import template

try:
    locale.setlocale(locale.LC_ALL, "id_ID.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "C.UTF-8")

register = template.Library()


@register.filter
def format_idr(value):
    try:
        value = float(value)
        return locale.currency(value, grouping=True, symbol="Rp ")
    except (ValueError, TypeError):
        return value
