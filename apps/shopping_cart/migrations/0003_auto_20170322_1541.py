# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0002_auto_20170322_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='total',
            field=models.FloatField(verbose_name='total productos'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='price',
            field=models.FloatField(),
        ),
    ]
