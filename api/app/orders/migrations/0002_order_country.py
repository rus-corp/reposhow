# Generated by Django 4.2.1 on 2023-09-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_docs', '0002_region_country'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.ManyToManyField(blank=True, related_name='countries', to='user_docs.country'),
        ),
    ]