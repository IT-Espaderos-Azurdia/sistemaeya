# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 04:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0011_auto_20170531_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='abono',
            name='banco',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='abono',
            name='operacionmes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.OperacionMes'),
        ),
    ]
