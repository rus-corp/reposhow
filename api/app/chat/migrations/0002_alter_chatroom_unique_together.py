# Generated by Django 4.2.1 on 2023-10-12 19:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chatroom',
            unique_together={('user_1', 'user_2')},
        ),
    ]
