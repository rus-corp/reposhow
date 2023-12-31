# Generated by Django 4.2.1 on 2023-10-13 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_remove_work_table_place_remove_work_time_spend'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='table_place',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Место в таблице'),
        ),
        migrations.AddField(
            model_name='work',
            name='time_spend',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Потраченное время в часах'),
        ),
    ]
