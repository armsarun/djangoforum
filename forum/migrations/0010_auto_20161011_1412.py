# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20161011_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
