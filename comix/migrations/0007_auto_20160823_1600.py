# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 16:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comix', '0006_auto_20160823_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
