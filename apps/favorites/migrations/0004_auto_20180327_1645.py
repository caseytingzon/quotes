# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-27 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0003_auto_20180327_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='favoriting_users',
        ),
        migrations.AddField(
            model_name='quote',
            name='favouriting_users',
            field=models.ManyToManyField(related_name='favourite_quotes', to='favorites.User'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_text',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
