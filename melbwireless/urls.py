from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (
        r'^maps/',
        include(
            'melbwireless.maps.urls',
            namespace='melbwireless',
            app_name='maps',
        ),
    ),
    (
        r'^admin/',
        include(admin.site.urls),
    ),
)
