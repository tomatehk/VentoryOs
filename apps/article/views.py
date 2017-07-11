from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
"""importamos a Seccion para saber todas las secciones que
tenemos para manipularlas"""
from ..section.models import Section
from ..utils import *
import psycopg2
# autenticacion
from django.contrib.auth.mixins import LoginRequiredMixin
# autorizacion por permission
from django.contrib.auth.mixins import PermissionRequiredMixin
# registro de aumentos
from .models import Increase
# paginador
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ArticleList(LoginRequiredMixin, View):
    """Mostramos todas los articulos url=^$"""
    template_name = 'article/index.html'

    def get(self, request):
        sections = Section.objects.all()

        return render(request, self.template_name, {'sections': sections})


class ArticleAdd(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Agregar articulos url=^add/(?P<section_id>[0-9]+)/$."""
    template_name = 'article/add.html'
    permission_required = 'section.add_section'

    def get(self, request, *args, **kwargs):
        # obtenemos el id para saber a que section agregaremos el problema
        section = Section.objects.get(pk=kwargs.get('section_id'))

        """conexion a la base de datos, para consultar y obtener columnas de
        la tabla"""
        try:
            connectdb = connectDb()
            cursor = connectdb.cursor()
            cursor.execute("SELECT * FROM " + str(section))
            details = [desc[0] for desc in cursor.description]

            description = getCOlumnsSort(details)

            connectdb.close()
            cursor.close()

            return render(request, self.template_name,
                          {'columns': description, 'section': section})

        except psycopg2.Error as e:
            return HttpResponse(str(e))

    def post(self, request, *args, **kwargs):
        section = str(Section.objects.get(pk=kwargs.get('section_id')))

        # Hacemos mutable para poder manipular POST
        request.POST._mutable = True

        # obtenemos las columnas de las filas en donde agregaremos datos
        columns = getColumns(section, True)

        # columnas ordenadas para un insert y eliminamos el id
        colums_sort = getCOlumnsSort(columns)
        parameters = ", ".join(["%s" for x in range(len(colums_sort))])

        # listamos los valores para introducilos en la base de datos
        list_t = []
        for x in colums_sort:
            list_t.append(request.POST[x])

        # ordenamos las columnas donde se agregaran los datos
        colums_sort = ", ".join([x for x in colums_sort])

        # convertimos los valores en una tupla para usarla en psycopg2
        values = list(list_t)
        values[-1] = str(round(float(values[-1]), 2))
        values = tuple(values)

        # conectamos a la base de datos
        connectdb = connectDb()
        cursor = connectdb.cursor()

        # tratamos de hacer los insert
        try:
            cursor.execute("INSERT INTO " + section + "(" + colums_sort +
                           ")" + " VALUES(" + parameters + ")", values)
            message = "¡Perfecto, producto agregado!"

        except psycopg2.Error:

            return JsonResponse(status=500)
        # afirmamos los cambios#
        connectdb.commit()
        connectdb.close()
        cursor.close()

        return JsonResponse({'message': message}, status=200)


class ArticleSearch(LoginRequiredMixin, View):
    """Vista de la busqueda de articulos url=^search/$"""
    template_name = 'article/search.html'

    def post(self, request, *args, **kwargs):
        # botenemos la palabra clave para la busqueda de el articulo en la base
        # de datos
        search = request.POST['search']

        # conectamos a la base de datos
        connectdb = connectDb()
        cursor = connectdb.cursor()

        # columnas de las secciones
        section_columns = dict()

        """un diccionario que tendra como key el nombre de la seccion
        y valor los resultados del search"""
        column_organized = dict()

        sections = Section.objects.all()
        for section in sections:
            # Obtenemos columnas
            columns = getColumns(section.name, True)
            """Comprobamos si existen columnas en lsa cuales podemos buscar
            (string)"""
            if len(columns) == 3:
                continue

            columns_sort = getCOlumnsSort(columns)
            colums_get = ", ".join(columns_sort)

            del columns_sort[-2:]
            columns_format = " OR ".join([columns_sort[i] + " LIKE '%" +
                                          search + "%'"
                                          for i in range(len(columns_sort))])
            try:
                cursor.execute("SELECT id," + colums_get + " FROM " +
                               section.name + " WHERE " + columns_format + " ORDER BY id ASC")

                results = cursor.fetchall()

                if results:
                    column_organized[section.name] = results

                    """hacemos referencia a la seccion y a sus columnas para
                    crear t."""
                    section_columns[section.name] = columns_sort

            except psycopg2.Error as e:
                return HttpResponse(e)

        # cerramos las conexiones
        cursor.close()
        connectdb.close()

        return render(request, self.template_name,
                      {'sections': column_organized,
                       'sections_columns': section_columns})


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Editamos articulos mediante post"""
    template_name = 'article/edit.html'
    permission_required = 'section.add_section'

    def post(self, request, *args, **kwargs):

        connectdb = connectDb()
        cursor = connectdb.cursor()

        if request.POST.get('edit', False):
            # id del articulo
            id = request.POST['edit']

            section = Section.objects.get(pk=request.POST['section']).name

            # Hacemos mutable para poder manipular POST
            request.POST._mutable = True

            # obtenemos las columnas de las filas en donde agregaremos datos
            columns = getColumns(section, True)

            # columnas ordenadas para un insert y eliminamos el id
            colums_sort = getCOlumnsSort(columns)

            # listamos los valores para introducilos en la base de datos
            list_t = []
            for x in colums_sort:
                list_t.append(request.POST[x])

            # ordenamos el set
            setter = list()

            for x in range(len(colums_sort)):
                # creamos un array para luego crear un string para la consulta sql
                if colums_sort[x] == 'precio':
                    setter.append(colums_sort[x] + " = '" + str(round(float(list_t[x]), 2)) + "'")
                else:
                    setter.append(colums_sort[x] + " = '" + list_t[x] + "'")

            setter = ", ".join([x for x in setter])

            try:
                sql = "UPDATE %s SET %s WHERE id = %i" % (section, setter, int(id))

                # ejecutamos la sentencia
                cursor.execute(sql)
                connectdb.commit()

                # cerramos la conexion
                cursor.close()
                connectdb.close()

            except psycopg2.Error as e:
                return JsonResponse(status=500)

            return JsonResponse({"message": "Perfecto articulo editado"}, status=200)

        else:
            # obtenemos la seccion
            section = Section.objects.get(name=request.POST['edit-article-section'])

            """conexion a la base de datos, para consultar y obtener columnas de
            la tabla"""
            try:
                cursor.execute("SELECT * FROM " + str(section))
                details = [desc[0] for desc in cursor.description]

                description = getCOlumnsSort(details)

                # columnas de las secciones
                section_columns = dict()

                """un diccionario que tendra como key el nombre de la seccion
                y valor los resultados del search"""
                column_organized = dict()

                columns = getColumns(section.name, True)

                columns_sort = getCOlumnsSort(columns)
                colums_get = ", ".join(columns_sort)

                del columns_sort[-2:]
                cursor.execute("SELECT id," + colums_get + " FROM " +
                               section.name + " WHERE id=" + request.POST['edit-article-id'])

                results = cursor.fetchall()

                if results:
                    column_organized[section.name] = results

                    """hacemos referencia a la seccion y a sus columnas para
                    crear t."""
                    section_columns[section.name] = columns_sort

                connectdb.close()
                cursor.close()

                return render(request, self.template_name,
                              {'columns': description, 'section': section,
                               'article': [[list(z) for z in y] for x, y in
                                           column_organized.items()]})

            except psycopg2.Error as e:
                return HttpResponse(str(e))


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Clase para elimar articulos y devuelve una repuesta json"""
    permission_required = 'section.add_section'

    def post(self, request, *args, **kwargs):
        id_article = request.POST['id_article']
        section = request.POST['section']

        # conectamos a la base de datos
        connectdb = connectDb()
        cursor = connectdb.cursor()

        try:
            cursor.execute("DELETE FROM " + section + " WHERE " +
                           "id=" + id_article)
        except psycopg2.Error:
            return JsonResponse(status=500)

        # afirmamos los cambios#
        connectdb.commit()
        connectdb.close()
        cursor.close()

        return JsonResponse({'message': 'Perfecto articulo eliminado'}, status=200)


class ArticleIncrease(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Incrementamos precios de articulos url=^increase/"""
    permission_required = 'section.add_section'
    template_name = 'article/increase.html'

    def get(self, request):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # obtenemos la accion a realizar
        section = request.POST['section']
        percentage = int(request.POST['percentage'])

        if section == 'all':
            for x in Section.objects.all():
                try:
                    increaseArticles(section=str(x), percentage=percentage)

                except psycopg2.Error as e:
                    return HttpResponse(str(e))
        else:
            try:
                increaseArticles(section, percentage)

            except psycopg2.Error as e:
                return HttpResponse(str(e))

        message = "¡Perfecto precios aumentados!"

        return render(request, self.template_name, {"message": message + " en " + str(percentage) +
                      "%"})


class ArticleIncreaseRegistry(PermissionRequiredMixin, LoginRequiredMixin, View):
    """Registro de todas las incrementaciones de precio"""
    permission_required = 'section.add_section'
    template_name = 'article/increase_registry.html'

    def get(self, request):
        all_increase = Increase.objects.all().order_by('-increase_date')
        paginator = Paginator(all_increase, 10)
        # obetenmos la pagina a mostrar
        page = request.GET.get('page')

        try:
            registry_increase = paginator.page(page)

        except PageNotAnInteger:
            # si la pagina no es un entero, volvemos a la primera pagina
            registry_increase = paginator.page(1)

        except EmptyPage:
            # si la pagina esta fuera de rango, vamos a la ultima pagina
            registry_increase = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'registry': registry_increase})


class ArticleAlerts(LoginRequiredMixin, View):
    """ALerts causadas por el minimum mode"""
    template_name = 'article/articles-alerts.html'

    def get(self, request):
        # verificamos si existen alertas
        if getAlerts():
            # conectamos a la base de datos
            connectdb = connectDb()
            cursor = connectdb.cursor()

            # columnas de las secciones
            section_columns = dict()

            """un diccionario que tendra como key el nombre de la seccion
            y valor los resultados del search"""
            column_organized = dict()

            alerts = getAlerts()

            # iteramos para obtener los nombres de las secciones
            for x in alerts[1]:
                # obtenemos la seccion
                section = Section.objects.get(pk=x)
                # Obtenemos columnas
                columns = getColumns(section.name, True)
                """Comprobamos si existen columnas en lsa cuales podemos buscar
                (string)"""
                if len(columns) == 3:
                    continue

                columns_sort = getCOlumnsSort(columns)
                colums_get = ", ".join(columns_sort)

                del columns_sort[-2:]

                try:
                    cursor.execute("SELECT id," + colums_get + " FROM " +
                                   section.name + " WHERE cantidad < " + str(section.minimum) +
                                   " ORDER BY id ASC")

                    results = cursor.fetchall()

                    if results:
                        column_organized[section.name] = results

                        """hacemos referencia a la seccion y a sus columnas para
                        crear t."""
                        section_columns[section.name] = columns_sort

                except psycopg2.Error as e:
                    return HttpResponse(e)
            # cerramos las conexiones
            cursor.close()
            connectdb.close()

            return render(request, self.template_name,
                          {'sections': column_organized,
                           'sections_columns': section_columns})

        else:
            return render(request, self.template_name)


class PrintInventory(LoginRequiredMixin, View):
    """Muestra el inventario para imprimir"""
    template_name = 'article/print_inventory.html'

    def get(self, request):
        # conectamos a la base de datos
        connectdb = connectDb()
        cursor = connectdb.cursor()

        # columnas de las secciones
        section_columns = dict()

        """un diccionario que tendra como key el nombre de la seccion
        y valor los resultados del search"""
        column_organized = dict()

        sections = Section.objects.all()
        for section in sections:
            # Obtenemos columnas
            columns = getColumns(section.name, True)
            """Comprobamos si existen columnas en lsa cuales podemos buscar
            (string)"""
            if len(columns) == 3:
                continue

            columns_sort = getCOlumnsSort(columns)
            colums_get = ", ".join(columns_sort)

            del columns_sort[-2:]

            try:
                cursor.execute("SELECT id," + colums_get + " FROM " +
                               section.name + " ORDER BY id ASC")

                results = cursor.fetchall()

                if results:
                    column_organized[section.name] = results

                    """hacemos referencia a la seccion y a sus columnas para
                    crear t."""
                    section_columns[section.name] = columns_sort

            except psycopg2.Error as e:
                return HttpResponse(e)

        # cerramos las conexiones
        cursor.close()
        connectdb.close()

        return render(request, self.template_name,
                      {'sections': column_organized,
                       'sections_columns': section_columns})
