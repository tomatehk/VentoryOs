from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from apps.utils import *
# verificar los usuarios por defectos estan creados
from django.contrib.auth.models import User


def reload_sections():
    return get_all_sections()


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    """filtro para las fechas"""
    return value.strftime(format)


def getUser():

    return User.objects.all()


def format_money(quantity):

    return "{:,.2f}".format(quantity)


def format_quantity(quantity):

    return "{:,d}".format(quantity)


def environment(**options):
    env = Environment(**options)
    env.filters['datetimeformat'] = datetimeformat
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'sections_all': reload_sections,
        'id': 0,
        'get_sales': get_sales,
        'get_total_money': get_total_money,
        'get_total_articles': get_total_articles,
        'get_user': getUser,
        'alerts': getAlerts,
        'format': format_money,
        'format_quantity': format_quantity,
        'get_total_money_articles': get_total_money_articles,
    })

    return env
