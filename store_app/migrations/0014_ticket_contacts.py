# Generated by Django 4.2.6 on 2023-11-13 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0013_alter_ticket_ticket_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='contacts',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
