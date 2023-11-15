# Generated by Django 4.2.1 on 2023-10-14 06:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_alter_work_table_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='time_spend',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Потраченное время в часах'),
        ),
    ]
