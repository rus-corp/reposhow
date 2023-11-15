# Generated by Django 4.2.1 on 2023-09-03 19:24

import app.portfolio.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('currency', models.CharField(choices=[('RUB', 'RUB'), ('USD', 'USD')], default='RUB', max_length=3, verbose_name='валюта цены заказа')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('period', models.DateField(blank=True, null=True, verbose_name='Срок выполнения')),
                ('slug', models.SlugField(max_length=255)),
                ('views', models.IntegerField(default=0)),
                ('target_audience', models.TextField(blank=True, max_length=300, verbose_name='Целевая аудитория')),
                ('atention', models.TextField(blank=True, max_length=300, verbose_name='Обратить внимание')),
                ('status', models.CharField(choices=[('MD', 'Moderation'), ('PB', 'Published'), ('AC', 'Accepted'), ('OE', 'On_Execution'), ('OA', 'On_Accepted'), ('CP', 'Comleted')], default='MD', max_length=2)),
                ('file1', models.FileField(blank=True, null=True, upload_to='order_files/%Y/%m/%d', validators=[app.portfolio.validators.file_size_validate])),
                ('file2', models.FileField(blank=True, null=True, upload_to='order_files/%Y/%m/%d', validators=[app.portfolio.validators.file_size_validate])),
                ('file3', models.FileField(blank=True, null=True, upload_to='order_files/%Y/%m/%d', validators=[app.portfolio.validators.file_size_validate])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_customers', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
                ('eur_acc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_eur_acc', to='accounts.account')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('executor_status', models.CharField(choices=[('NS', 'No_Status'), ('CN', 'Candidate'), ('EX', 'Executor')], default='NS', max_length=2)),
                ('text', models.TextField(blank=True, max_length=500, null=True, verbose_name='Текст отклика')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Стоимость выполнения')),
                ('term', models.DateField(blank=True, null=True, verbose_name='Срок выполнения')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата отклика')),
                ('file1', models.FileField(blank=True, null=True, upload_to='order_responses/%Y/%m/%d', verbose_name='Файл1')),
                ('file2', models.FileField(blank=True, null=True, upload_to='order_responses/%Y/%m/%d', verbose_name='Файл2')),
                ('file3', models.FileField(blank=True, null=True, upload_to='order_responses/%Y/%m/%d', verbose_name='Файл3')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_responses', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_responses', to='orders.order')),
            ],
            options={
                'verbose_name': 'Отклик на заказ',
                'verbose_name_plural': 'Отклики на заказ',
            },
        ),
        migrations.CreateModel(
            name='OrderResponseComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file1', models.FileField(blank=True, null=True, upload_to='order_response_comments/%Y/%m/%d', verbose_name='Файл1')),
                ('file2', models.FileField(blank=True, null=True, upload_to='order_response_comments/%Y/%m/%d', verbose_name='Файл2')),
                ('file3', models.FileField(blank=True, null=True, upload_to='order_response_comments/%Y/%m/%d', verbose_name='Файл3')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('order_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_response_comments', to='orders.orderresponse', verbose_name='Отклик')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='replies', to='orders.orderresponsecomment', verbose_name='родитель комментария')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_response_comments', to=settings.AUTH_USER_MODEL, verbose_name='Оставил комметарий')),
            ],
            options={
                'verbose_name': 'Отклик на заказ',
                'verbose_name_plural': 'Отклики на заказы',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='executor',
            field=models.ManyToManyField(blank=True, through='orders.OrderResponse', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='rub_acc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_rub_acc', to='accounts.account'),
        ),
        migrations.AddField(
            model_name='order',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_specializations', to='categories.specialization'),
        ),
        migrations.AddField(
            model_name='order',
            name='usd_acc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_usd_acc', to='accounts.account'),
        ),
    ]
