# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-04 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0002_auto_20161004_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]
