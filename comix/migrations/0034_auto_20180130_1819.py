# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-30 18:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comix', '0033_auto_20180129_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='gcd_publisher',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='gcd_series',
        ),
        migrations.DeleteModel(
            name='Publisher',
        ),
        migrations.DeleteModel(
            name='Series',
        ),
    ]
