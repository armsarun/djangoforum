# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0039_auto_20170201_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(upload_to='users/%Y/%m/%d'),
        ),
    ]
