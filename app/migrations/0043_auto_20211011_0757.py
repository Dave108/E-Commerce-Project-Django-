# Generated by Django 3.2.7 on 2021-10-11 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20211011_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='kart',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='items',
            field=models.ManyToManyField(to='app.Kart'),
        ),
    ]