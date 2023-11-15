# Generated by Django 4.2.1 on 2023-09-07 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_docs', '0002_region_country'),
        ('main_users', '0002_userinfo_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_countries', to='user_docs.country'),
        ),
    ]