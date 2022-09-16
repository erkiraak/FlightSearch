# Generated by Django 4.1 on 2022-09-16 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_result_departure_airlines_result_return_airlines_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airline',
            name='iata_code',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='search',
            name='departure_date',
            field=models.DateField(default=datetime.date(2022, 9, 30)),
        ),
        migrations.AlterField(
            model_name='search',
            name='limit',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='search',
            name='max_stopovers',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='return_date',
            field=models.DateField(blank=True, default=datetime.date(2022, 10, 7), null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='search_type',
            field=models.CharField(choices=[('fixed', 'Fixed dates'), ('duration', 'Cheapest flights between dates ')], default='strict', max_length=10),
        ),
    ]
