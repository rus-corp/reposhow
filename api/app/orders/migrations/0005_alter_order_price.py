# Generated by Django 4.2.1 on 2023-10-24 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderresponsecomment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]