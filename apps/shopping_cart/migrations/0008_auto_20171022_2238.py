# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-23 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0007_auto_20171022_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='id_check',
            field=models.IntegerField(null=True, verbose_name='id sale'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
