from django.conf.urls import url
from .views import *

app_name = 'shopping_cart'
urlpatterns = [
    url(r'^view_cart/$', ShoppingCart.as_view(), name='view_cart'),
    url(r'^buy/$', Buy.as_view(), name='buy'),
    url(r'^sales_record/$', SalesRecord.as_view(), name='sales_record'),
    url(r'^information/$', Information.as_view(), name='information'),
]
