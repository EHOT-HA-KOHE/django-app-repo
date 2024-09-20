from django import template


register = template.Library()

@register.filter()
def format_number(value):
    try:
        value = int(value)
        if value >= 1_000_000:
            return f"{value // 1_000_000}M"
        elif value >= 1_000:
            return f"{value // 1_000}K"
        else:
            return str(value)
    except (TypeError, ValueError):
        return value
