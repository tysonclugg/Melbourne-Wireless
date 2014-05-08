from melbwireless.maps.models import Node
import simplejson
from  django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

def compat_map_view(request):
    try:
        node_id = request.GET['id']
    except KeyError:
        try:
            node_id = request.GET['ID']
        except KeyError:
            node_id = request.META['QUERY_STRING']
    return HttpResponseRedirect(
        reverse('melbwireless:node_view', kwargs={'pk': node_id.upper()}),
    )


def node_json(request):
    return HttpResponse(
        simplejson.dumps(
            dict(
                (
                    node.id,
                    {
                        'lat': node.latitude,
                        'lon': node.longitude,
                        'alt': node.altitude,
                        'owner': node.owner.name,
                    },
                )
                for node
                in Node.objects.filter(
                    id__startswith = 'A',
                )
            ),
            indent=4,
        ),
        content_type='text/json',
    )
