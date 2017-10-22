from django.conf.urls import url
from .views import *

app_name = 'user'

urlpatterns = [
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^config$', Config.as_view(), name='config'),
    url(r'^contact$', Contact.as_view(), name='contact'),
    url(r'^active$', active, name='active'),
]
