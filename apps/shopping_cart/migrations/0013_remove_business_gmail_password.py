# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-24 02:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0012_auto_20171023_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='gmail_password',
        ),
    ]
