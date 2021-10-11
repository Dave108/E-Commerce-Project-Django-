# Generated by Django 3.2.7 on 2021-10-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_orderplaced_delivered'),
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
