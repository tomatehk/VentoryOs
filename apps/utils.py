import psycopg2
# importmaos para agregar al registro de incrementaciones
from .article.models import Increase
from django.utils import timezone
from apps.section.models import Section
# importamos modelo para saber cuantas ventas se an realizado
from apps.shopping_cart.models import Sale
from django.db.models import Sum


def getColumns(section, id):
    """Funcion para obtener columnas de una tabla"""
    connectdb = connectDb()
    cursor = connectdb.cursor()
    cursor.execute("SELECT * FROM " + section)
    connectdb.commit()
    # obtenemos la descripcion de las columnas
    if id:
        desc = [desc[0] for desc in cursor.description]
    else:
        desc = [desc[0] for desc in cursor.description if desc[0] != 'id']

    connectdb.close()
    cursor.close()

    return desc


def getCOlumnsSort(details):
    """FUncion para obtener las columnas ordenadas"""

    # obtenemos columnas ordenadas aleatoriamente para mostrar correctamente
    details_temp = [x for x in reversed(details[3:])]
    # obetenmos las 3 columnas base id, catidad, precio
    details = [details[x] for x in range(3)]

    for z in range(len(details_temp)):
        details.insert(1, details_temp[z])

    del details[0]

    return details


def connectDb():
    """Connexion rapida por via psycopg"""
    try:
        connectdb = psycopg2.connect(
            database='ventoryos', user='postgres',
            password='storemg', host='localhost'
        )
    except psycopg2.Error as e:
        return e

    return connectdb


def increaseArticles(section, percentage):
    """Funcion para aumentar precios"""
    # conectamos a la base de datos
    connectdb = connectDb()
    cursor = connectdb.cursor()

    cursor.execute("SELECT id, precio FROM " + section)

    # tomamos todos los id
    todo = cursor.fetchall()
    for z in todo:
        # hacemos el calculo y modificamo el precio aumentado su precio
        new_price = ((float(z[1]) * percentage) / 100) + float(z[1])
        cursor.execute(
            "UPDATE " + section + " SET precio=%s WHERE id=%s",
            (round(new_price, 2), z[0])
        )

    # agregamos al registro de incrementos
    increase_reg = Increase(section=section, increase=percentage, increase_date=timezone.now())
    increase_reg.save()

    # commit y cerramos conexiones de las bases de datos
    connectdb.commit()
    cursor.close()
    connectdb.close()


def getAlerts():
    """Obtenemos el numero de alertas y las secciones con alertas"""
    sections = Section.objects.filter(minimum_mode=True)

    alerts = 0
    sections_alert = []
    minimum_mode_active = False
    for x in sections:
        if x.minimum_mode:
            minimum_mode_active = True
            # agregamos a la sections a el array que contiene las secciones con alertas
            sections_alert.append(x.id)

            # conectamos a la base de datos
            conectdb = connectDb()
            cursor = conectdb.cursor()
            # realizamos el string que sera la consulta
            query = "SELECT id, cantidad FROM %s WHERE cantidad <= %i" % (x.name, x.minimum)
            cursor.execute(query)
            result = cursor.fetchall()

            # agreamos el numero de alertas
            alerts += len(result)

    if minimum_mode_active:
        return 0 if alerts == 0 else [alerts, sections_alert]


def get_all_sections():
    """Obtenemos todas las secciones"""
    sections = Section.objects.all()

    return sections


def get_sales():
    """Obtenemos todas las ventas"""
    sales = len(Sale.objects.all())
    return sales


def get_total_money():
    """Obtenemos el total de dinero hecho"""
    total = Sale.objects.all().aggregate(Sum('price'))

    return float((total['price__sum'])) if total['price__sum'] else 0.00


def get_total_money_ef():
    """Obtenemos el total de dinero hecho"""
    total = Sale.objects.filter(type_pay='ef').aggregate(Sum('price'))

    return float((total['price__sum'])) if total['price__sum'] else 0.00


def get_total_money_po():
    """Obtenemos el total de dinero hecho"""
    total = Sale.objects.filter(type_pay='po').aggregate(Sum('price'))

    return float((total['price__sum'])) if total['price__sum'] else 0.00


def get_total_money_articles():
    """Obtenemos todo el dinero existen en articulos"""
    sections = get_all_sections()

    # conectamos a la base de datos
    conectdb = connectDb()
    cursor = conectdb.cursor()

    # variable que tendra el total
    total = 0

    for x in sections:
        # sql para la consulta
        sql = "SELECT SUM(precio*cantidad) FROM %s" % x.name
        cursor.execute(sql)
        result = cursor.fetchone()
        
        # verificamos si existen articulos para sumar
        if result[0]:
            total += result[0]

    return total


def get_total_articles():
    """Obtenemos todo el dinero existen en articulos"""
    sections = get_all_sections()

    # conectamos a la base de datos
    conectdb = connectDb()
    cursor = conectdb.cursor()

    # variable que tendra el total
    total = 0

    for x in sections:
        # sql para la consulta
        sql = "SELECT SUM(cantidad) FROM %s" % x.name
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result[0]:
            total += result[0]

    return total
