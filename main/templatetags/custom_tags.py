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



@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
