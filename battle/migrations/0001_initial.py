# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 04:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.Battle')),
            ],
        ),
        migrations.CreateModel(
            name='Fighter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.Battle')),
                ('figther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.Fighter')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.User')),
            ],
        ),
        migrations.AddField(
            model_name='fighter',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='figther',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.Fighter'),
        ),
        migrations.AddField(
            model_name='battle',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battle.User'),
        ),
        migrations.AddField(
            model_name='battle',
            name='fighters',
            field=models.ManyToManyField(to='battle.Fighter'),
        ),
    ]
