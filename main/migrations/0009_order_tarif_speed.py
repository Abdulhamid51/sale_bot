# Generated by Django 5.1 on 2025-02-08 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20250205_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=200)),
                ('service_id', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=1000)),
                ('count', models.CharField(max_length=200)),
                ('remains', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('charge', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='tarif',
            name='speed',
            field=models.IntegerField(default=0, verbose_name='Скорость'),
        ),
    ]
