# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='total productos'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
