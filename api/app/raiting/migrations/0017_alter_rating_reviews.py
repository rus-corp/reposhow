# Generated by Django 4.2.1 on 2023-11-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raiting', '0016_alter_rating_arbit_alter_rating_contest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='reviews',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', verbose_name='Кол-во отзывов:'),
        ),
    ]