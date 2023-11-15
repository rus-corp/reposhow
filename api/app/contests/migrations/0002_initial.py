# Generated by Django 4.2.1 on 2023-09-03 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0001_initial'),
        ('categories', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='contestresponsecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_response_comments', to=settings.AUTH_USER_MODEL, verbose_name=''),
        ),
        migrations.AddField(
            model_name='contestresponse',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_responses', to='contests.contest', verbose_name=''),
        ),
        migrations.AddField(
            model_name='contestresponse',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contest_responses', to=settings.AUTH_USER_MODEL, verbose_name=''),
        ),
        migrations.AddField(
            model_name='contestappfiles',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_files', to='contests.contest', verbose_name=''),
        ),
        migrations.AddField(
            model_name='contest',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_activities', to='categories.activity', verbose_name='Сфера деятельности'),
        ),
        migrations.AddField(
            model_name='contest',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_categories', to='categories.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='contest',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_customers', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик'),
        ),
        migrations.AddField(
            model_name='contest',
            name='eur_acc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contest_eur_acc', to='accounts.account'),
        ),
        migrations.AddField(
            model_name='contest',
            name='executor',
            field=models.ManyToManyField(blank=True, through='contests.ContestResponse', to=settings.AUTH_USER_MODEL, verbose_name='Исполнители'),
        ),
        migrations.AddField(
            model_name='contest',
            name='rub_acc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contest_rub_acc', to='accounts.account'),
        ),
        migrations.AddField(
            model_name='contest',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_specializations', to='categories.specialization', verbose_name='Специализация'),
        ),
        migrations.AddField(
            model_name='contest',
            name='usd_acc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contest_usd_acc', to='accounts.account'),
        ),
    ]
