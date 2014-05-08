from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from melbwireless.maps.models import Node

def with_compat(view, old_url_format):
    view.old_url_format = old_url_format
    return view

urlpatterns = patterns('melbwireless.maps.views',
    url(
        r'^json/',
        'node_json',
    ),
    url(
        r'^view/(?P<pk>[A-Za-z]{3})/$',
        with_compat(
            DetailView.as_view(
                model = Node,
                template_name = 'maps/view.html',
            ),
            '/maps/view?{pk}',
        ),
        name='node_view',
    ),
    # Compatibility URLs to match with old site URLs.
    url(
        # /maps/view?gho /maps/view?id=gho /maps/view.php?id=gho ...etc.
        r'^view(?:.php)?$',
        'compat_map_view',
        name='old_node_view',
    ),
)
