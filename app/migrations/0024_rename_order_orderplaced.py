# Generated by Django 3.2.7 on 2021-10-08 06:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0023_auto_20211007_1442'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderPlaced',
        ),
    ]
