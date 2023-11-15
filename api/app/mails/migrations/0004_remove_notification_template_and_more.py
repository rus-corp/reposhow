# Generated by Django 4.2.1 on 2023-09-25 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_alter_notification_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='template',
        ),
        migrations.AddField(
            model_name='notification',
            name='extra_classification',
            field=models.CharField(blank=True, choices=[('for_freelancers', 'News for freelancers'), ('for_customers', 'News for customers'), ('for_founders', 'News for founders'), ('for_all', 'News for all')], null=True, verbose_name='Дополнительные параметры для уведомлений:'),
        ),
        migrations.AddField(
            model_name='notification',
            name='template_link',
            field=models.TextField(default=1, max_length=100, verbose_name='Шаблон для отправки сообщения:'),
            preserve_default=False,
        ),
    ]
