# Generated by Django 4.2.1 on 2023-11-03 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adv_cash', '0002_blacklisttransactionshash'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blacklisttransactionshash',
            options={'ordering': ('-created_at',), 'verbose_name': 'Черный список хэшей транзакций', 'verbose_name_plural': 'Черный список хэшей транзакций'},
        ),
        migrations.AlterModelTable(
            name='blacklisttransactionshash',
            table='black_list_transaction_hash',
        ),
    ]
