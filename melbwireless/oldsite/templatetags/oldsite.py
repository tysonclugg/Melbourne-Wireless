from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def oldurl(context):
    request = context['request']
    resolver_match = request.resolver_match
    try:
        path = resolver_match.func.old_url_format.format(**resolver_match.kwargs)
    except AttributeError:
        path = request.path
    return 'http://www.melbournewireless.org.au{0}'.format(path)
