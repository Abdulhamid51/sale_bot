# Generated by Django 5.1 on 2025-02-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_order_tarif_speed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='for_test',
            field=models.BooleanField(default=False),
        ),
    ]
