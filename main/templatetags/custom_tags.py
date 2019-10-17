from django import template
from django.urls import reverse, NoReverseMatch
import re
from django.urls import resolve
register = template.Library()
from main.choices import ACTIVE

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()


@register.simple_tag
def active(request, urls):
    """
    {% navactive request "view_name another_view_name" %}
    if view name not exsist error

    {% active request "dashboard" %}
    """
    url_name = resolve(request.path).url_name
    if url_name in urls.split():
        return "active"
    return ""


@register.simple_tag
def active_menu(request, urls):
    """
    {% navactive request "view_name another_view_name" %}
    if view name not exsist error

    {% active request "dashboard" %}
    """
    url_name = resolve(request.path).url_name
    if url_name in urls.split():
        return "active menu-open"
    return ""

@register.filter()
def range(min=5):
    return range(min)

@register.filter
def count_active(value):
    return value.filter(status=ACTIVE).count()

@register.simple_tag
def divide(x, y):
    try:
        return float(x) / float(y)
    except (ValueError, ZeroDivisionError):
        return None

@register.simple_tag
def mul(x, y):
    try:
        return float(x) * float(y)
    except (ValueError):
        return None

from decimal import Decimal
@register.filter
# {{ credit.credit_limit|subtract:credit.credit_balance }}
# value came as str for me
def subtract(value, arg):
    final = Decimal(value) - Decimal(arg)
    final = float(final)
    print(final)
    formated = '{0:.5g}'.format(final)
    print(formated)
    return formated
