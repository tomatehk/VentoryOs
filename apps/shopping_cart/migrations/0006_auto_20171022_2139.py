# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-23 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0005_auto_20170402_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='section',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='sale',
            name='article',
            field=models.CharField(max_length=200),
        ),
    ]