# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0007_auto_20170527_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='docfile',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
