# Generated by Django 2.0.2 on 2018-02-10 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_report', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
