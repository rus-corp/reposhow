# Generated by Django 4.2.1 on 2023-09-16 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_docs', '0004_notifications'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notifications',
        ),
    ]