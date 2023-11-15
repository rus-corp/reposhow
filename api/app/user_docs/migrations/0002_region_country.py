# Generated by Django 4.2.1 on 2023-09-03 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_docs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('phone_code', models.CharField(blank=True, max_length=15, null=True)),
                ('flag', models.FileField(blank=True, null=True, upload_to='flags/')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='countries', to='user_docs.region')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
    ]
