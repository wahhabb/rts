# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 17:29
from __future__ import unicode_literals

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20160904_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=localflavor.us.models.USStateField(),
        ),
    ]
