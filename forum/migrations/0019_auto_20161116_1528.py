# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-16 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0018_post_closed_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='closed_reason',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
