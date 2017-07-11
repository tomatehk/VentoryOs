"""
Urls para app_seccion
"""
from django.conf.urls import url
# Inportamos todas las vistas
from .views import *

app_name = 'section'

urlpatterns = [
    url(r'^$', SectionList.as_view(), name='sections'),
    url(r'^add/$', SectionAdd.as_view(), name='add'),
    url(r'^(?P<pk>[0-9]+)/information/$', SectionInformation.as_view(),
        name='information'),
    url(r'^(?P<pk>[0-9]+)/update/$', SectionUpdate.as_view(), name='update'),
]
