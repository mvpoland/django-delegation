try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from .views import result


urlpatterns = patterns('',
    url(r'^result/(?P<dg_id>\d+)/$', result, name='django_delegation_result'),
)
