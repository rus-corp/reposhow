# Generated by Django 4.2.1 on 2023-10-20 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='purpose_of_payment',
            field=models.CharField(choices=[('EF', 'Вступительный взнос пользователя'), ('RF', 'Реферальные бонусы'), ('ND', 'Не востребованный платеж'), ('CO', 'Создание заказа'), ('TU', 'Перевод между юзерами')], max_length=20, verbose_name='назначение платежа'),
        ),
    ]
