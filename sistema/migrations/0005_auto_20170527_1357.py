# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0004_auto_20170527_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='descripcion_estatus',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='entrego',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='recibio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]