# Generated by Django 4.1 on 2022-09-02 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_alter_search_limit_alter_search_user'),
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
