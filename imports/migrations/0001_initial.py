# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-29 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GcdBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year_began', models.IntegerField(blank=True, null=True)),
                ('year_ended', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('issue_count', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('reserved', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('year_began_uncertain', models.IntegerField()),
                ('year_ended_uncertain', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'gcd_brand',
            },
        ),
        migrations.CreateModel(
            name='GcdIndiciaPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year_began', models.IntegerField(blank=True, null=True)),
                ('year_ended', models.IntegerField(blank=True, null=True)),
                ('is_surrogate', models.IntegerField()),
                ('notes', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('issue_count', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('reserved', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('year_began_uncertain', models.IntegerField()),
                ('year_ended_uncertain', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'gcd_indicia_publisher',
            },
        ),
        migrations.CreateModel(
            name='GcdIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('volume', models.CharField(max_length=50)),
                ('no_volume', models.IntegerField()),
                ('display_volume_with_number', models.IntegerField()),
                ('indicia_pub_not_printed', models.IntegerField()),
                ('no_brand', models.IntegerField()),
                ('publication_date', models.CharField(max_length=255)),
                ('key_date', models.CharField(max_length=10)),
                ('sort_code', models.IntegerField()),
                ('price', models.CharField(max_length=255)),
                ('page_count', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('page_count_uncertain', models.IntegerField()),
                ('indicia_frequency', models.CharField(max_length=255)),
                ('no_indicia_frequency', models.IntegerField()),
                ('editing', models.TextField()),
                ('no_editing', models.IntegerField()),
                ('notes', models.TextField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('reserved', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('is_indexed', models.IntegerField()),
                ('isbn', models.CharField(max_length=32)),
                ('valid_isbn', models.CharField(max_length=13)),
                ('no_isbn', models.IntegerField()),
                ('variant_name', models.CharField(max_length=255)),
                ('barcode', models.CharField(max_length=38)),
                ('no_barcode', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('no_title', models.IntegerField()),
                ('on_sale_date', models.CharField(max_length=10)),
                ('on_sale_date_uncertain', models.IntegerField()),
                ('rating', models.CharField(max_length=255)),
                ('no_rating', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'gcd_issue',
            },
        ),
        migrations.CreateModel(
            name='GcdPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year_began', models.IntegerField(blank=True, null=True)),
                ('year_ended', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('is_master', models.IntegerField()),
                ('imprint_count', models.IntegerField()),
                ('brand_count', models.IntegerField()),
                ('indicia_publisher_count', models.IntegerField()),
                ('series_count', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('issue_count', models.IntegerField()),
                ('reserved', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('year_began_uncertain', models.IntegerField()),
                ('year_ended_uncertain', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'gcd_publisher',
            },
        ),
        migrations.CreateModel(
            name='GcdSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sort_name', models.CharField(max_length=255)),
                ('format', models.CharField(max_length=255)),
                ('year_began', models.IntegerField()),
                ('year_began_uncertain', models.IntegerField()),
                ('year_ended', models.IntegerField(blank=True, null=True)),
                ('year_ended_uncertain', models.IntegerField()),
                ('publication_dates', models.CharField(max_length=255)),
                ('is_current', models.IntegerField()),
                ('tracking_notes', models.TextField()),
                ('notes', models.TextField()),
                ('publication_notes', models.TextField()),
                ('has_gallery', models.IntegerField()),
                ('open_reserve', models.IntegerField(blank=True, null=True)),
                ('issue_count', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('reserved', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('has_indicia_frequency', models.IntegerField()),
                ('has_isbn', models.IntegerField()),
                ('has_barcode', models.IntegerField()),
                ('has_issue_title', models.IntegerField()),
                ('has_volume', models.IntegerField()),
                ('is_comics_publication', models.IntegerField()),
                ('color', models.CharField(max_length=255)),
                ('dimensions', models.CharField(max_length=255)),
                ('paper_stock', models.CharField(max_length=255)),
                ('binding', models.CharField(max_length=255)),
                ('publishing_format', models.CharField(max_length=255)),
                ('has_rating', models.IntegerField()),
                ('publication_type_id', models.IntegerField(blank=True, null=True)),
                ('is_singleton', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'gcd_series',
            },
        ),
        migrations.CreateModel(
            name='StddataCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'stddata_country',
            },
        ),
        migrations.CreateModel(
            name='StddataLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'stddata_language',
            },
        ),
        migrations.CreateModel(
            name='TblComics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.CharField(max_length=1)),
                ('cat_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=255)),
                ('series', models.CharField(max_length=255)),
                ('gcd_series_id', models.IntegerField()),
                ('gcd_series_url', models.CharField(max_length=255)),
                ('gcd_issue_id', models.IntegerField()),
                ('gcd_issue_url', models.CharField(max_length=255)),
                ('gcd_publisher_id', models.IntegerField()),
                ('gcd_publisher_url', models.CharField(max_length=255)),
                ('publisher', models.CharField(max_length=255)),
                ('gcd_publisher_id_2', models.IntegerField()),
                ('gcd_publisher_url_2', models.CharField(max_length=255)),
                ('thumbnail', models.CharField(max_length=255)),
                ('thumbnail2', models.CharField(max_length=255)),
                ('thumbnail3', models.CharField(max_length=255)),
                ('thumbnail4', models.CharField(max_length=255)),
                ('thumbnail5', models.CharField(max_length=255)),
                ('thumbnail6', models.CharField(max_length=255)),
                ('thumbnail7', models.CharField(max_length=255)),
                ('thumbnail8', models.CharField(max_length=255)),
                ('thumbnail9', models.CharField(max_length=255)),
                ('thumbnail10', models.CharField(max_length=255)),
                ('bigimage', models.CharField(db_column='bigImage', max_length=255)),
                ('scarcity_note', models.CharField(db_column='Scarcity_Note', max_length=255)),
                ('type', models.CharField(db_column='Type', max_length=255)),
                ('title_notes', models.CharField(db_column='Title_Notes', max_length=255)),
                ('issue_notes', models.CharField(max_length=255)),
                ('grade_notes', models.CharField(db_column='Grade_Notes', max_length=255)),
                ('indicia_date', models.CharField(db_column='Indicia_Date', max_length=255)),
                ('status', models.CharField(db_column='Status', max_length=255)),
                ('catalog_no', models.CharField(db_column='Catalog_No', max_length=255)),
                ('mark', models.CharField(db_column='Mark', max_length=255)),
                ('issue_text', models.CharField(db_column='Issue_Text', max_length=255)),
                ('edition', models.CharField(db_column='Edition', max_length=255)),
                ('sort_title', models.CharField(db_column='Sort_Title', max_length=255)),
                ('near_grade', models.CharField(db_column='Near_Grade', max_length=255)),
                ('inserts', models.CharField(db_column='Inserts', max_length=255)),
                ('issue', models.IntegerField()),
                ('ceritifcate_no', models.CharField(db_column='Ceritifcate_No', max_length=255)),
                ('year', models.IntegerField(db_column='Year')),
                ('nm_price', models.CharField(db_column='NM_Price', max_length=255)),
                ('cover_price', models.CharField(db_column='Cover_price', max_length=255)),
                ('si', models.CharField(db_column='SI', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nm', models.CharField(db_column='NM', max_length=255)),
                ('single_quantity', models.CharField(db_column='Single_Quantity', max_length=255)),
                ('cost', models.CharField(db_column='Cost', max_length=255)),
                ('overstreet_0', models.CharField(db_column='Overstreet_0', max_length=255)),
                ('packs', models.CharField(db_column='Packs', max_length=255)),
                ('no_per_pack', models.CharField(db_column='No_Per_Pack', max_length=255)),
                ('overstreet_01_price', models.CharField(db_column='Overstreet_01_Price', max_length=255)),
                ('bar_code_price', models.CharField(db_column='Bar_Code_Price', max_length=255)),
                ('title_code', models.CharField(db_column='Title_Code', max_length=255)),
                ('overstreet_02', models.CharField(db_column='Overstreet_02', max_length=255)),
                ('vol_no', models.IntegerField(db_column='Vol_No')),
                ('collection_no', models.CharField(db_column='Collection_No', max_length=255)),
                ('numerical_grade', models.DecimalField(db_column='Numerical_Grade', decimal_places=3, max_digits=10)),
                ('overstreet_03', models.CharField(db_column='Overstreet_03', max_length=255)),
                ('overstreet_04', models.CharField(db_column='Overstreet_04', max_length=255)),
                ('variance', models.CharField(max_length=255)),
                ('publication', models.CharField(max_length=255)),
                ('story', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('inker', models.CharField(max_length=255)),
                ('writer', models.CharField(max_length=255)),
                ('type_of_cover', models.CharField(max_length=255)),
                ('condition', models.CharField(max_length=255)),
                ('first_appearance', models.CharField(max_length=255)),
                ('origin_of_story', models.CharField(max_length=255)),
                ('page_quality', models.CharField(max_length=255)),
                ('is_featured', models.CharField(max_length=1)),
                ('description', models.CharField(max_length=255)),
                ('pagetitle', models.CharField(db_column='pageTitle', max_length=255)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.CharField(max_length=255)),
                ('sortorder', models.IntegerField(db_column='sortOrder')),
                ('auto_url', models.CharField(max_length=1)),
                ('is_active', models.CharField(max_length=1)),
                ('added_date', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'tbl_comics',
            },
        ),
    ]
