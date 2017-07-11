from django.db import models


class Increase(models.Model):
    section = models.CharField('name section', max_length=100)
    increase = models.IntegerField('percentage increase', default=0)
    increase_date = models.DateTimeField('date increase')

    class Meta:
        db_table = "app_article_increase"

    def __str__(self):
        return self.section
