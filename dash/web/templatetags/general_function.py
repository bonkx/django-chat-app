from django import template
from django.conf import settings
from django.contrib.humanize.templatetags import humanize

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %} outputs ?foo=one&bar=two&baz=99

    A RequestContext is required for access to the current querystring.
    """
    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def multiply(value, arg):
    return float(str(value).replace(",", "")) * float(str(arg).replace(",", ""))


@register.filter
def subtract(value, arg):
    return float(str(value).replace(",", "")) - float(str(arg).replace(",", ""))


@register.filter()
def replace_commas(value):
    return str(value).replace(",", ".")


@register.filter
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'rb', 'jt', 'tr', 'qu'][magnitude])


@register.filter()
def to_grams(value):
    if value is None:
        return "-"
    grams = float(str(value).replace(",", "")) * 1000
    # print("{:.0f}".format(grams))
    return "{:.0f} gr".format(grams)


@register.filter()
def convert_weight(value):
    # value = gram
    if value is None:
        return "-"
    if value >= 1000000:  # ton = 1000grx1kgx1000kg
        ton = float(str(value).replace(",", "")) / 1000000
        return "{:.1f} ton".format(ton)
    # if value >= 100000:  # kw = 1000grx1kgx100kg
    #     kw = float(str(value).replace(",", "")) / 100000
    #     return "{:.1f} kw".format(kw)
    if value >= 1000:  # kg = 1000grx1kg
        kg = float(str(value).replace(",", "")) / 1000
        return "{:.1f} kg".format(kg)

    grams = float(str(value).replace(",", ""))
    return "{:.0f} gr".format(grams)
