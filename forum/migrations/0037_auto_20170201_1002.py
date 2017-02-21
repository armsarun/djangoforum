# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 10:02
from __future__ import unicode_literals

from django.db import migrations
import validatedfile.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0036_auto_20170131_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=validatedfile.fields.ValidatedFileField(upload_to='users/%Y/%m/%d'),
        ),
    ]