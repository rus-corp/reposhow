# Generated by Django 4.2.1 on 2023-10-25 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raiting', '0012_rating_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='summary',
        ),
    ]