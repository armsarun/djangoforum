# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0021_auto_20161205_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Announcement', 'Announcement'), ('Bug Report', 'Bug Report'), ('Tips and tricks', 'Tips and tricks'), ('General', 'General')], default='General', max_length=255),
        ),
    ]
