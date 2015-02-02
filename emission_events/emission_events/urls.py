from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from emissions.views import *


urlpatterns = patterns(
    '',
    url(r'^$', home_view),
    url(r'^search/', search_view),
    url(r'^regulated-entity/(?P<pk>\d+)/', regulated_entity_view, name=u'entity_detail'),
    url(r'^county/(?P<county_name>\w+)/', county_view, name=u'county_detail'),
    url(r'^admin/', include(admin.site.urls)),
)
