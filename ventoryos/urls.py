"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.section.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('apps.user.urls')),
    url(r'^$', DefaultView.as_view(), name="default"),
    url(r'^section/', include('apps.section.urls')),
    url(r'^article/', include('apps.article.urls')),
    url(r'^shopping/', include('apps.shopping_cart.urls')),
]
