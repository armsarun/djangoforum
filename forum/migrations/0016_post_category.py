# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-30 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_auto_20161023_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('AN', 'Announcement'), ('BR', 'Bug Report'), ('TT', 'Tips and tricks'), ('GR', 'General')], default='GR', max_length=2),
        ),
    ]
