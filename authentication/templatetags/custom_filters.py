from django import template
import locale

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')  # set idr format

register = template.Library()

@register.filter
def format_idr(value):
    try:
        value = float(value)
        return locale.currency(value, grouping=True, symbol="Rp ")
    except (ValueError, TypeError):
        return value 
