# Generated by Django 3.2.7 on 2021-10-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20211008_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditems',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]