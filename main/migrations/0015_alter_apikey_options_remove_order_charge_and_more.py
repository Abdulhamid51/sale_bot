# Generated by Django 5.1 on 2025-02-13 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_apikey'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apikey',
            options={'verbose_name': 'API-ключ', 'verbose_name_plural': 'API-ключи'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='charge',
        ),
        migrations.RemoveField(
            model_name='order',
            name='count',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='publication',
        ),
        migrations.RemoveField(
            model_name='order',
            name='remains',
        ),
        migrations.RemoveField(
            model_name='order',
            name='service_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='url',
        ),
        migrations.AddField(
            model_name='apikey',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.client'),
        ),
        migrations.AddField(
            model_name='order',
            name='orders',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tarif',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.tarif'),
        ),
    ]
