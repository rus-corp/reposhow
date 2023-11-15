# Generated by Django 4.2.1 on 2023-09-03 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('RUB', 'Рубли'), ('USD', 'Доллары США'), ('EUR', 'Евро')], default='RUB', max_length=3, verbose_name='валюта счета')),
                ('account_name', models.CharField(max_length=55, unique=True, verbose_name='Cчёт')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'счёт',
                'verbose_name_plural': 'счета',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('RUB', 'RUB'), ('USD', 'USD')], default='RUB', max_length=3, verbose_name='валюта операции')),
                ('purpose_of_payment', models.CharField(choices=[('EF', 'Вступительный взнос пользователя'), ('RF', 'Реферальные бонусы'), ('ND', 'Не востребованный платеж'), ('CO', 'Создание заказа')], max_length=2, verbose_name='назначение платежа')),
                ('summ', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма')),
                ('time_operation', models.DateTimeField(auto_now_add=True, verbose_name='время операции')),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_acc', to='accounts.account', verbose_name='счёт списания')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_acc', to='accounts.account', verbose_name='счёт зачисления')),
            ],
            options={
                'verbose_name': 'транзакция',
                'verbose_name_plural': 'транзакции',
                'ordering': ('-time_operation',),
            },
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='наименование фонда')),
                ('eur_account', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='eur_fund', to='accounts.account', verbose_name='Счет EUR')),
                ('rub_account', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rub_fund', to='accounts.account', verbose_name='Счет RUB')),
                ('usd_account', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='usd_fund', to='accounts.account', verbose_name='Счет USD')),
            ],
            options={
                'verbose_name': 'фонд',
                'verbose_name_plural': 'фонды',
            },
        ),
    ]
