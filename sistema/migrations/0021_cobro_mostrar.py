# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-15 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0020_expediente_autenticafirma'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobro',
            name='mostrar',
            field=models.BooleanField(default=True),
        ),
    ]