# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-15 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comix', '0016_auto_20161002_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='variants',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]