# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comix', '0009_auto_20160828_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(db_index=True, max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comix.Issue')),
            ],
            options={
                'ordering': ['date_added'],
                'db_table': 'cart_items',
            },
        ),
    ]
