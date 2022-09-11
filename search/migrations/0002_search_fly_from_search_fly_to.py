# Generated by Django 4.1 on 2022-09-06 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='fly_from',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='search_fly_from', to='search.airport', verbose_name='Origin airport'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='fly_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='search_fly_to', to='search.airport', verbose_name='Destination airport'),
            preserve_default=False,
        ),
    ]
