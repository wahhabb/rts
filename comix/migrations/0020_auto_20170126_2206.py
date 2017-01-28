# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-26 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comix', '0019_auto_20170126_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='edition',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='in_gcd_flag',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='scarcity_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='in_gcd_flag',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='series',
            name='in_gcd_flag',
            field=models.BooleanField(default=True),
        ),
    ]