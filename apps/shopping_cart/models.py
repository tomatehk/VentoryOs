from django.db import models


class Client(models.Model):
    EFECTIVE = "ef"
    POINT = "po"

    TYPE_PAY_CHOICE = (
        (EFECTIVE, 'efective'),
        (POINT, 'point'),
    )

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField('name client', max_length=200)
    total = models.FloatField('total productos', null=False)
    # tipo de pago, usando un choice
    type_pay = models.CharField('tipo de pago', max_length=2,
                                choices=TYPE_PAY_CHOICE, default=EFECTIVE)

    class Meta:
        db_table = 'app_shopping_cart_client'

    def __str__(self):

        return self.name


class Sale(models.Model):
    article = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price = models.FloatField('total productos', null=False)
    pub_date = models.DateTimeField('date published')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'app_shopping_cart_sale'

    def __str__(self):
        return self.article
