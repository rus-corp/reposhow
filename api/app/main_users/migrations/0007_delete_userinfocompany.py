# Generated by Django 4.2.1 on 2023-09-20 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_users', '0006_rename_experiense_userinfo_experience'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInfoCompany',
        ),
    ]
