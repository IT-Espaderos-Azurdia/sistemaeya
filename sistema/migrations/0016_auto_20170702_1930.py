# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0015_empresa_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='password',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
