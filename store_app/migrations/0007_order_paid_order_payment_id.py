# Generated by Django 4.2.6 on 2023-10-17 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0006_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
