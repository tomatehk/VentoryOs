from django.db import models


class Section(models.Model):
    name = models.CharField("name table", max_length=100, unique=True)
    minimum_mode = models.BooleanField("minimum mode", default=False)
    minimum = models.IntegerField("minimum", default=0)

    class Meta:
        db_table = 'app_section'

    def __str__(self):

        return self.name
