# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-26 03:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0019_expediente_numeroexpe'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='autenticafirma',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
