# Generated by Django 4.1 on 2022-09-14 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_rename_code_airline_iata_code_remove_result_airlines_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='local_arrival',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='local_departure',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='return_flight',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='search',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='segment_no',
        ),
    ]