# Introduciendo vistas genericas
from django.http import JsonResponse, HttpResponseRedirect
# reverse para redireccionar
from django.urls import reverse
from django.views.generic import (ListView,)
from django.views import View
# Importamos la clase para guardar la nueva seccion
from .models import Section
# Importamos el modulo psycopg para hacer conexiones a la base de datos
import psycopg2
# importamos para crear el diccionario
import yaml
from collections import OrderedDict
# importamos shorcuts para implementar algunas de sus funciones
from django.shortcuts import render
# utilidades creadasx
from ..utils import *
# autenticacion
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ventoryos.settings import *


class DefaultView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    redirect_field_name = 'redirect_to=233'
    template_name = 'section/default.html'

    def get(self, request):
        return render(request, self.template_name)


class SectionList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """Lista de las secciones creadas url=r'^$'"""
    model = Section
    context_object_name = 'sections'
    template_name = 'section/index.html'
    permission_required = 'section.add_section'


class SectionAdd(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Agregar seccion url=r'^add/'"""
    permission_required = 'section.add_section'

    def post(self, request, *args, **kwargs):
        "Capturamos el nombre para la seccion"
        name = str(request.POST['section_name']).lower().replace(' ', '_')

        # conectamos en la base de datos
        try:
            connectdb = connectDb()
            cursor = connectdb.cursor()
            # agregamos una columnan id para refereirnos a los articulos
            cursor.execute("CREATE TABLE " + name + "(id SERIAL PRIMARY KEY, "
                           "cantidad int, precio float)")
            connectdb.commit()
            cursor.close()
            connectdb.close()

            # agregamos a la referencia de las secciones
            section = Section(name=name)
            section.save()
            message = '¡Perfecto se agrego la nueva seccion!'

        except psycopg2.Error:
            return JsonResponse(status=500)

        return JsonResponse({'message': message}, status=200)


class SectionInformation(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Informacion detallada de la seccion
    url = r'^(?P<pk>[0-9])/information/'"""
    template_name = 'section/information.html'
    permission_required = 'section.add_section'

    def get(self, request, *args, **kwargs):
        # obtenemos la seccion
        section = Section.objects.get(pk=kwargs.get('pk'))

        # obtenemos descripcion
        details = getColumns(str(section), True)

        # obtenemos las columnas ya ordenadas con nuestra funcion creada
        total_detail = getCOlumnsSort(details)

        return render(request, self.template_name, {'details': total_detail,
                                                    'section': section})


class SectionUpdate(PermissionRequiredMixin, LoginRequiredMixin, View):
    """"Agregamos campos a la seccion url=r'^(?P<pk>[0-9])/update/'"""
    model = Section
    permission_required = 'section.add_section'

    def post(self, request, *args, **kwargs):
        # obtenemos al objeto(tabla en la base de datos)
        id = kwargs.get('pk')
        section_table = str(Section.objects.get(pk=id)).lower()

        # Conectamos a la db para luego hacer cambios
        connectdb = connectDb()
        cursor = connectdb.cursor()
        type_function = request.POST['type']

        if type_function == 'delete':
            # obtenemos el nombre de la columna
            column = request.POST['values']

            try:
                cursor.execute("ALTER TABLE " + section_table +
                               " DROP COLUMN " + column)

            except psycopg2.Error:
                return JsonResponse(status=500)

            message = "¡Perfecto campo eliminado!"
        elif type_function == 'add':
            """Capturamos el nombre del campo y creamos un diccionario para
            manipularlo y poder crear sentencias sql"""
            values = request.POST['values']
            new = "{'" + \
                values.replace("&", "', '").replace("=", "': '") + "'}"
            ob = yaml.load(new)
            ob.pop('values')
            ob.pop('csrfmiddlewaretoken')
            object_organized = OrderedDict(sorted(ob.items()))

            # contendra las columnas nuevas de la tabla
            fields = []

            for key, value in object_organized.items():
                if key[:4] == 'name':
                    fields.append(value.lower() + " varchar(200)")

            try:
                for field in fields:
                    cursor.execute('ALTER TABLE ' + section_table + ' ADD ' +
                                   field + ";")
                    message = "¡Perfecto campo agregado! "
                    "<i class='fa fa-check-circle'></i>"

            except psycopg2.Error:
                return JsonResponse(status=500)

        elif type_function == 'delete-section':

            try:
                Section.objects.get(pk=id).delete()
                cursor.execute("DROP TABLE " + section_table)
                message = '!Perfecto seccion eliminada¡'

            except psycopg2.Error:
                return JsonResponse(status=500)

        elif type_function == 'minimum':
            # obtenemos la seccion
            section = Section.objects.get(pk=id)

            # obtenemos datos enviados por post
            if request.POST.get('minimum_mode', False) == 'on':
                minimum_mode = True if request.POST['minimum_mode'] == 'on' else False
                minimum = request.POST['min-number']
                # hacemos cambios en la seccion
                section.minimum_mode = minimum_mode
                section.minimum = minimum
            else:
                section.minimum_mode = False

            section.save()

            return HttpResponseRedirect(reverse('section:information', args=[id]))
        else:
            column = request.POST['values']
            new_name = request.POST['new_name'].lower().replace(" ", "_")

            try:
                cursor.execute("ALTER TABLE " + section_table + " RENAME " +
                               column + " TO " + new_name)
                message = '¡Perfecto campo renombrado!'

            except psycopg2.Error:
                return JsonResponse({'message': "error won"}, status=500)

        connectdb.commit()
        connectdb.close()
        cursor.close()

        return JsonResponse({'message': message}, status=200)
