# Generated by Django 4.2.1 on 2023-09-15 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raiting', '0005_rename_raitingcalculateconstant_ratingcalculateconstant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratingcalculateconstant',
            old_name='reviews',
            new_name='review_negative',
        ),
        migrations.AddField(
            model_name='ratingcalculateconstant',
            name='review_postive',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
