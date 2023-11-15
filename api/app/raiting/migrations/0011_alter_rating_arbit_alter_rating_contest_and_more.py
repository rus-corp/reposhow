# Generated by Django 4.2.1 on 2023-09-20 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raiting', '0010_rating_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='arbit',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Кол-во арбитражей:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='contest',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Кол-во учрежденных или посещенных контестов:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='orders',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Кол-во заказов:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='peace_orders',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Кол-во мировых соглашений:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='reg_time',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Время пошедшее с момента регистрации'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='reply_time',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Продолжительность ответа на оффер:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='reviews',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Кол-во отзывов:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='vote_participation',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Участие в голосованиях:'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='wins',
            field=models.IntegerField(blank=True, help_text='поле можно оставить пустым', null=True, verbose_name='Кол-во побед в контестах:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='arbit',
            field=models.IntegerField(verbose_name='Арбитражей:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='contest',
            field=models.IntegerField(verbose_name='Контестов созданных/посещенных:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='orders',
            field=models.IntegerField(verbose_name='Заказов:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='peace_orders',
            field=models.IntegerField(verbose_name='Мировых соглашений:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='reg_time',
            field=models.IntegerField(verbose_name='Месяцев с момента регистрации:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='reply_time_1_hour',
            field=models.IntegerField(verbose_name='Ответ на оффер в течение часа:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='reply_time_6_hour',
            field=models.IntegerField(verbose_name='Ответ на оффер в течение 6 часов'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='reply_time_more',
            field=models.IntegerField(verbose_name='Ответ на оффер ≥12 часов'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='review_negative',
            field=models.IntegerField(verbose_name='Негативный отзыв:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='review_positive',
            field=models.IntegerField(verbose_name='Позитивный отзыв:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='vote_ignore',
            field=models.IntegerField(verbose_name='Игнор голосования:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='vote_participation',
            field=models.IntegerField(verbose_name='Участие в голосовании:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='wins_1_place',
            field=models.IntegerField(verbose_name='Победа в контесте:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='wins_2_place',
            field=models.IntegerField(verbose_name='Второе место в контесте:'),
        ),
        migrations.AlterField(
            model_name='ratingcalculateconstant',
            name='wins_3_place',
            field=models.IntegerField(verbose_name='Третье место в контесте:'),
        ),
    ]