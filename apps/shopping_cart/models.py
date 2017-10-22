from django.db import models


class Client(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField('name client', max_length=200)
    total = models.FloatField('total productos', null=False)

    class Meta:
        db_table = 'app_shopping_cart_client'

    def __str__(self):

        return self.name


class Sale(models.Model):
    EFECTIVE = "ef"
    POINT = "po"

    TYPE_PAY_CHOICE = (
        (EFECTIVE, 'efective'),
        (POINT, 'point'),
    )

    id_check = models.IntegerField('id sale', null=True)
    section = models.CharField(max_length=100, null=False, default="")
    article = models.CharField(max_length=200, null=False)
    quantity = models.IntegerField()
    price = models.FloatField('total productos', null=False)
    pub_date = models.DateTimeField('date published')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # tipo de pago, usando un choice
    type_pay = models.CharField('tipo de pago', max_length=2,
                                choices=TYPE_PAY_CHOICE, default=EFECTIVE)

    class Meta:
        db_table = 'app_shopping_cart_sale'

    def __str__(self):
        return self.article

class Business(models.Model):
    name = models.CharField(max_length=150)
    it = models.CharField(max_length=150)
