# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comix', '0005_publisher_issue_ct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='catalog_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='gcd_notes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='grade_notes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='indicia_date',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='inserts',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issue_text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='notes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='publication_date',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='si',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='issue',
            name='sold_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='volume',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='series',
            name='color',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='series',
            name='notes',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
