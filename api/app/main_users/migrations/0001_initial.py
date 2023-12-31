# Generated by Django 4.2.1 on 2023-09-03 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('categories', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('username', models.CharField(blank=True, db_index=True, max_length=55, unique=True, verbose_name='Ник пользователя')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email')),
                ('email_confirm', models.BooleanField(default=False, verbose_name='Почта подтверждена')),
                ('paid_entrance_rub', models.BooleanField(default=False, verbose_name='Оплатил вступительный взнос в RUB')),
                ('paid_entrance_usd', models.BooleanField(default=False, verbose_name='Оплатил вступительный взнос в USD')),
                ('paid_entrance_eur', models.BooleanField(default=False, verbose_name='Оплатил вступительный взнос в EUR')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Дата вступления')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный пользователь')),
                ('status', models.CharField(choices=[('CS', 'Customer'), ('FR', 'Freelancer'), ('FC', 'Freelancer_candidate'), ('CC', 'Customer_candidate')], default='FC', max_length=2, verbose_name='Статус')),
                ('founder', models.BooleanField(blank=True, default=False, verbose_name='Основатель')),
                ('slug', models.SlugField(blank=True, max_length=155, unique=True)),
                ('referal_link', models.CharField(blank=True, max_length=150, verbose_name='реферальная ссылка')),
                ('legal_status', models.CharField(choices=[('PS', 'Physical'), ('LG', 'Legal')], default='PS', max_length=2, verbose_name='юридический статус')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('eur_acc', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='eur_acc', to='accounts.account', verbose_name='Счет EUR')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to=settings.AUTH_USER_MODEL, verbose_name='Пригласивший')),
                ('rub_acc', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rub_acc', to='accounts.account', verbose_name='Счет RUB')),
                ('usd_acc', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='usd_acc', to='accounts.account', verbose_name='Счет USD')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=155, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, db_index=True, max_length=155, null=True, verbose_name='Фамилия')),
                ('father_name', models.CharField(blank=True, max_length=155, null=True, verbose_name='Отчество')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='users/avatar/%Y/%m/%d', verbose_name='Аватар')),
                ('on_vacation', models.BooleanField(default=False, null=True, verbose_name='Отпуск')),
                ('adress', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес проживания')),
                ('skill', models.TextField(blank=True, null=True, verbose_name='Навыки')),
                ('review_ratio', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Звездность')),
                ('experiense', models.CharField(blank=True, max_length=100, null=True, verbose_name='Опыт')),
                ('cost_of_hour_work', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Стоимость часа работы')),
                ('profile_description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание профиля')),
                ('baner', models.FileField(blank=True, null=True, upload_to='users/baners/%Y/%m/%d', verbose_name='Банер')),
            ],
            options={
                'verbose_name': 'Данные пользователя',
                'verbose_name_plural': 'Данные пользователей',
            },
        ),
        migrations.CreateModel(
            name='UserSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False)),
                ('specialization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_specializations', to='categories.specialization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_specializations', to='main_users.userinfo')),
            ],
            options={
                'verbose_name': 'Специализация юзера',
                'verbose_name_plural': 'Специализации юзера',
            },
        ),
        migrations.CreateModel(
            name='UserInfoCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(db_index=True, max_length=100, verbose_name='Полное название компании')),
                ('short_company_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Короткое название компании')),
                ('ceo_name', models.CharField(max_length=150, verbose_name='ФИО руководителя')),
                ('ceo_post', models.CharField(blank=True, max_length=100, null=True, verbose_name='Должность руководителя')),
                ('adress_in_law', models.CharField(blank=True, max_length=200, null=True, verbose_name='Юр. адрес')),
                ('adress_fact', models.CharField(blank=True, max_length=200, null=True, verbose_name='Физ. адрес')),
                ('reg_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='ОГРН')),
                ('company_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='ИНН')),
                ('kpp_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='КПП')),
                ('certificate', models.CharField(blank=True, max_length=30, null=True, verbose_name='Свидетельство номер')),
                ('certificate_file', models.FileField(blank=True, null=True, upload_to='company_docs/%Y/%m/%d', verbose_name='Свидетельство файл')),
                ('company_site', models.CharField(blank=True, max_length=80, null=True, verbose_name='Сайт компании')),
                ('company_phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Телефон компании')),
                ('company_email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email компании')),
                ('social_site', models.CharField(blank=True, max_length=80, null=True, verbose_name='Социальные сети')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_info', to='main_users.userinfo')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.AddField(
            model_name='userinfo',
            name='specialization',
            field=models.ManyToManyField(through='main_users.UserSpecialization', to='categories.specialization'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EmailToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации')),
                ('key', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Токен')),
                ('purpose', models.CharField(choices=[('confirm', 'Подтверждение регистрации'), ('email', 'Смена email'), ('reset_link', 'Ссылка сброса пароля'), ('reset', 'Сброс пароля')], default='confirm', max_length=10, verbose_name='Назначение')),
                ('number_of_checks', models.PositiveSmallIntegerField(default=0, verbose_name='Number of checks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_token', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, связанный с токеном')),
            ],
            options={
                'verbose_name': 'Токен Email',
                'verbose_name_plural': 'Токены Email',
                'db_table': 'EmailToken',
            },
        ),
    ]
