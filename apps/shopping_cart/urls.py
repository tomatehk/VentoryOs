from django.conf.urls import url
from .views import *

app_name = 'shopping_cart'
urlpatterns = [
    url(r'^view_cart/$', ShoppingCart.as_view(), name='view_cart'),
    url(r'^buy/$', Buy.as_view(), name='buy'),
    url(r'^sales_record/$', SalesRecord.as_view(), name='sales_record'),
    url(r'^sales_record/print/$', SalesRecordPrint.as_view(), name='sales_record_print'),
    url(r'^check_print/(?P<id_check>[0-9]+)/$', CheckPrint.as_view(), name='check_print'),
    url(r'^check_print_pdf/(?P<id_check>[0-9]+)/$', CheckPrintPdf.as_view(), name='check_print_pdf'),
    url(r'^sale_delete/(?P<pk>[0-9]+)/$', SaleDelete.as_view(), name='sale_delete'),
    url(r'^information/$', Information.as_view(), name='information'),
]
