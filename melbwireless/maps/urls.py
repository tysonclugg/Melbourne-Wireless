from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from melbwireless.maps.models import Node

def with_attrs(obj, *reg_callbacks, **attrs):
    for name, val in attrs.items():
        setattr(obj, name, val)
    for reg_callback in reg_callbacks:
        reg_callback(obj)
    return obj

urlpatterns = patterns('melbwireless.maps.views',
    url(
        r'^json/',
        'node_json',
    ),
    url(
        r'^view/(?P<pk>[A-Za-z]{3})/$',
        with_attrs(
            DetailView.as_view(
                model = Node,
                template_name = 'maps/view.html',
            ),
            old_url_format = '/maps/view?{pk}',
            title = lambda pk: 'Node {0}'.format(pk.upper()),
            parent = 'maps',
        ),
        name='maps_view_node',
    ),
    url(
        r'^node/(?P<pk>[A-Za-z]{3})/$',
        with_attrs(
            DetailView.as_view(
                model = Node,
                template_name = 'maps/view.html',
            ),
            old_url_format = '/maps/view?{pk}',
            title = lambda pk: 'Node {0}'.format(pk.upper()),
            parent = 'maps',
        ),
        name='maps_node_view',
    ),
    # Compatibility URLs to match with old site URLs.
    url(
        # /maps/view?gho /maps/view?id=gho /maps/view.php?id=gho ...etc.
        r'^view(?:.php)?$',
        'compat_map_view',
        name='old_node_view',
    ),
)
