from melbwireless.maps import models

def db(request):
    return {
        'nodes': models.Node.objects.all(),
    }
