# Generated by Django 3.2.7 on 2021-10-08 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_checkoutaddress_save_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='payment_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.payment'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='payment_choice',
            field=models.CharField(choices=[('CD', 'Cash on Delivery'), ('NB', 'Net Banking'), ('UPI', 'UPI'), ('DC', 'Debit Card'), ('CC', 'Credit Card')], max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_choice',
            field=models.CharField(choices=[('CD', 'Cash on Delivery'), ('NB', 'Net Banking'), ('UPI', 'UPI'), ('DC', 'Debit Card'), ('CC', 'Credit Card')], max_length=20),
        ),
    ]
