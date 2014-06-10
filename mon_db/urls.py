from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mon_db import views

urlpatterns = patterns('',
    url(r'^$', views.overview, name='index'),
    url(r'^overview$', views.overview, name='overview'),
    url(r'^detail$', views.detail, name='detail')
)
