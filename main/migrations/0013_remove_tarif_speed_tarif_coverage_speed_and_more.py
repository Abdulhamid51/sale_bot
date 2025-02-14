# Generated by Django 5.1 on 2025-02-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_order_publication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarif',
            name='speed',
        ),
        migrations.AddField(
            model_name='tarif',
            name='coverage_speed',
            field=models.IntegerField(default=0, verbose_name='Скорость. Охват'),
        ),
        migrations.AddField(
            model_name='tarif',
            name='like_speed',
            field=models.IntegerField(default=0, verbose_name='Скорость. Лайков'),
        ),
        migrations.AddField(
            model_name='tarif',
            name='saved_speed',
            field=models.IntegerField(default=0, verbose_name='Скорость. Сохраненные'),
        ),
    ]
