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
from django.urls import reverse_lazy, reverse
# paginador
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
# sumar precios de articulos
from django.db.models import Sum
from django.core.mail import EmailMessage
import pdfkit
from django.conf import settings


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
                # verificamos si el campo nombre esta vacio
                if not client:
                    return JsonResponse(status=500)

                client = Client(id=c_i, name=client, total=total)
                client.save()
            else:
                client = Client.objects.get(id=c_i)

            # verificamos las ventas del cliente para poder
            # generar facturas
            try:
                # id que tendra la factura
                id = client.sale_set.latest('id').id_check + 1
            except Sale.DoesNotExist:
                id = 1

            for x in articles['articles']:
                client.sale_set.create(
                    id_check=id,
                    section=x[4],
                    article=x[1],
                    quantity=x[2],
                    price=x[3],
                    pub_date=timezone.now(),
                    type_pay=type_pay,
                )
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

            return render(
                request,
                'shopping_cart/client_search.html',
                {'client': client, 'total': total['price__sum'], 'sales': sales}
            )
        else:
            return render(request, 'shopping_cart/client_search.html')


class SalesRecordPrint(LoginRequiredMixin, View):
    template_name = 'shopping_cart/sales_record_print.html'

    def get(self, request):
        registry = Sale.objects.all().order_by('-pub_date')

        return render(request, self.template_name, {'registry': registry})


class CheckPrint(View):
    template_name = 'shopping_cart/check_print.html'

    def get(self, request, id_check):
        # obtenemos los articulos con ese id de factura
        registry = Sale.objects.filter(id_check=id_check)

        # total
        total = 0
        for x in registry:
            total += x.price

        try:
            business = Business.objects.get(pk=1)
            # verificamos si hay internet para poder enviar pdfs
            # http = urllib3.PoolManager()
            # r = http.request('GET', 'http://google.com')
            # internet = True
        except Business.DoesNotExist:
            business = False

        # except urllib3.exceptions.MaxRetryError:
            # internet = False

        return render(
            request, self.template_name,
            {
                'registry': registry, 
                'total': total,
                'business': business,
            }
        )

    def post(self, request, *args, **kwargs):
        business = Business.objects.get(pk=1)
        message = "Usted a realizado una compra en: \n %s \n it: %s" % (
            business.name,
            business.it
        )
        send_to = request.POST['send_to']
        html_to_pdf = request.POST['html_to_pdf']

        # numero de la factura
        check_number = request.POST['check_number'] + '.pdf'
        # generate pdf to send
        pdfkit.from_string(html_to_pdf, 'checks/' + check_number)

        email = EmailMessage(
            'Factura/compra',
            message,
            settings.EMAIL_HOST_USER,
            [send_to],
            headers = {'Reply-To': settings.EMAIL_HOST_USER},
        )
        # agregamos el pdf para enviarlo
        email.attach_file('checks/' + check_number)
        email.send()

        return JsonResponse({'message': 'perfecto'}, status=200)


class CheckPrintPdf(View):
    template_name = 'shopping_cart/check_print_pdf.html'

    def get(self, request, id_check):
        # obtenemos los articulos con ese id de factura
        registry = Sale.objects.filter(id_check=id_check)

        # total
        total = 0
        for x in registry:
            total += x.price

        try:
            business = Business.objects.get(pk=1)
        except Business.DoesNotExist:
            business = False

        return render(
            request, self.template_name,
            {
                'registry': registry, 
                'total': total,
                'business': business,
            }
        )


class SaleDelete(LoginRequiredMixin, DeleteView):
    template_name = 'shopping_cart/sale_delete.html'
    model = Sale
    context_object_name = 'sale'
    success_url = reverse_lazy('shopping_cart:sales_record')


class Information(LoginRequiredMixin, View):
    template_name = "shopping_cart/information.html"

    def get(self, request):

        return render(request, self.template_name)
