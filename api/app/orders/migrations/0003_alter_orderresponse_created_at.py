# Generated by Django 4.2.1 on 2023-09-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderresponse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика'),
        ),
    ]
