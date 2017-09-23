# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0013_auto_20170601_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='autenticadpi',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expediente',
            name='autenticafirma',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expediente',
            name='constanciaingresos',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expediente',
            name='formularios',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='tenencias',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]