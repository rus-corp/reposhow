# Generated by Django 4.2.1 on 2023-10-29 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_users', '0014_userinfo_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('date_joined',), 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
