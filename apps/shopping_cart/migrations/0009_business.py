# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-23 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0008_auto_20171022_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('rif', models.CharField(max_length=150)),
            ],
        ),
    ]
