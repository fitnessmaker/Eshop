# Generated by Django 4.2.6 on 2023-11-14 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0015_ticket_bag'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='Battery',
            field=models.BooleanField(blank=True, default=False, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='Charger',
            field=models.BooleanField(blank=True, default=False, max_length=25, null=True),
        ),
    ]
