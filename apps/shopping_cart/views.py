from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import *
import yaml
# importamos utilidades
from ..utils import *
import psycopg2
# autenticacion
from django.contrib.auth.mixins import LoginRequiredMixin
# vista para el delete
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
# paginador
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
# sumar precios de articulos
from django.db.models import Sum


class ShoppingCart(LoginRequiredMixin, View):
    template_name = 'shopping_cart/index.html'

    def get(self, request):

        return render(request, self.template_name)


class Buy(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # obtenemos los articulos y lo tranformamos en una lista
        articles = yaml.load(request.POST['articles'])
        client = request.POST['name']
        c_i = request.POST['c_i']
        type_pay = request.POST['type_pay']
        total = request.POST['total']

        # conectamos a la base de datos
        conectdb = connectDb()
        cursor = conectdb.cursor()

        try:
            if not Client.objects.filter(id=c_i):
                client = Client(id=c_i, name=client, total=total,
                                type_pay=type_pay)
                client.save()
            else:
                client = Client.objects.get(id=c_i)

            for x in articles['articles']:
                    client.sale_set.create(article=x[1], quantity=x[2],
                                           price=x[3], pub_date=timezone.now())
                    # obtenemos el total de articulo que existen para descontar
                    cursor.execute("SELECT cantidad from " + x[-1] + " WHERE id=" + str(x[0]))
                    total = cursor.fetchall()
                    cursor.execute("UPDATE " + x[-1] + " SET cantidad=" + str(total[0][0] - x[2]) +
                                   " WHERE id=" + str(x[0]))
            client.save()

            conectdb.commit()
            cursor.close()
            conectdb.close()

            message = '¡Venta realizada con exito!'
            return JsonResponse({'message': message}, status=200)

        except psycopg2.Error:
            return JsonResponse(status=500)

        except Exception:
            return JsonResponse(status=500)


class SalesRecord(LoginRequiredMixin, View):
    template_name = 'shopping_cart/sales.html'

    def get(self, request):
        registry = Sale.objects.all().order_by('-pub_date')
        paginator = Paginator(registry, 30)
        # obtenmos la pagina a mostrar
        page = request.GET.get('page')

        try:
            registry_page = paginator.page(page)

        except PageNotAnInteger:
            # si la pagina no es un entero, volvemos a la primera pagina
            registry_page = paginator.page(1)

        except EmptyPage:
            # si la pagina esta fuera de rango, vamos a la ultima pagina
            registry_page = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'registry': registry_page})

    def post(self, request, *args, **kwargs):
        # obtenemos la cedula del cliente
        c_i = request.POST['c-i']

        if Client.objects.filter(id=c_i):
            client = Client.objects.get(id=c_i)
            total = client.sale_set.aggregate(Sum('price'))
            # obtenemos todas las ventas realizadas por el cliente
            sales = client.sale_set.all().order_by('-pub_date')

            return render(request, 'shopping_cart/client_search.html',
                          {'client': client, 'total': total['price__sum'], 'sales': sales})
        else:
            return render(request, 'shopping_cart/client_search.html')


class SaleDelete(LoginRequiredMixin, DeleteView):
    template_name = 'shopping_cart/sale_delete.html'
    model = Sale
    context_object_name = 'sale'
    success_url = reverse_lazy('shopping_cart:sales_record')


class Information(LoginRequiredMixin, View):
    template_name = "shopping_cart/information.html"

    def get(self, request):

        return render(request, self.template_name)
