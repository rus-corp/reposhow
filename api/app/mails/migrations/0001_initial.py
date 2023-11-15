# Generated by Django 4.2.1 on 2023-09-23 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMailPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_refill', models.BooleanField(default=False, verbose_name='Увед. о пополнении аккаунта:')),
                ('customers_offers', models.BooleanField(default=False, verbose_name='Увед. о предложениях заказчиков:')),
                ('freelancers_responses', models.BooleanField(default=False, verbose_name='Увед. об откликах заказчиков:')),
                ('reviews', models.BooleanField(default=False, verbose_name='Увед. об отзывах:')),
                ('votes', models.BooleanField(default=False, verbose_name='Увед. о голосованиях:')),
                ('chat', models.BooleanField(default=False, verbose_name='Увед. о пополнении аккаунта:')),
                ('news', models.BooleanField(default=False, verbose_name='Увед. о пополнении аккаунта:')),
                ('user', models.ForeignKey(help_text='выберите подходящего пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='mails', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь:')),
            ],
        ),
    ]