from django.conf.urls import url
from .views import *

app_name = 'article'

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='articles'),
    url(r'^add/(?P<section_id>[0-9]+)/$', ArticleAdd.as_view(), name='add'),
    url(r'^search/$', ArticleSearch.as_view(), name='search'),
    url(r'^edit/$', ArticleEdit.as_view(), name='edit'),
    url(r'^delete/$', ArticleDelete.as_view(), name='delete'),
    url(r'^increase/$', ArticleIncrease.as_view(), name='increase'),
    url(r'^increases/registry/$', ArticleIncreaseRegistry.as_view(), name='increase_registry'),
    url(r'^alerts/$', ArticleAlerts.as_view(), name='article_alerts'),
    url(r'^print/$', PrintInventory.as_view(), name='print_inventory'),
]
