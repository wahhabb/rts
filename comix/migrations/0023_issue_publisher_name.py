# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-31 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comix', '0022_auto_20170128_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='publisher_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
