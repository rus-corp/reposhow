from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator
import uuid
from django.contrib.auth.validators import UnicodeUsernameValidator

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from app.accounts.models import Account, Fund
from app.accounts.operations import (
    transfer_money,
    amount_father_rub,
    amount_father_usd,
    grandfather_amount_rub,
    grandfather_amount_usd,
    grand_grandfather_amount_rub,
    grand_grandfather_amount_usd,
    generate_account_number
)
from app.reviews.models import Review
from app.raiting.models import Rating
from app.categories.models import Specialization
from app.user_docs.models import Country


class CustomUserManager(BaseUserManager):
    """Создает и сохраняет пользователя с введенным им email и паролем."""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email должен быть указан"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, MPTTModel):
    """Стандартная модель юзера, прописана в настройках"""

    class Status(models.TextChoices):
        CUSTOMER = "CS", "Customer"
        FREELANCER = "FR", "Freelancer"
        FREELANCER_CANDIDATE = "FC", "Freelancer_candidate"
        CUSTOMER_CANDIDATE = "CC", "Customer_candidate"

    class LegalStatus(models.TextChoices):
        PHYSICAL = "PS", "Physical"
        LEGAL = "LG", "Legal"

    username = models.CharField(
        _("Ник пользователя"), max_length=55, unique=True, db_index=True, blank=True
    )
    email = models.EmailField(_("Email"), unique=True, db_index=True)
    email_confirm = models.BooleanField(_("Почта подтверждена"), default=False)

    """оплачен вступительный взнос"""
    paid_entrance_rub = models.BooleanField(
        _("Оплатил вступительный взнос в RUB"), default=False
    )
    paid_entrance_usd = models.BooleanField(
        _("Оплатил вступительный взнос в USD"), default=False
    )
    paid_entrance_eur = models.BooleanField(
        _("Оплатил вступительный взнос в EUR"), default=False
    )

    date_joined = models.DateField(_("Дата вступления"), auto_now_add=True)
    is_active = models.BooleanField(_("Активный пользователь"), default=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Пригласивший"),
        related_name="children",
    )

    status = models.CharField(
        _("Статус"),
        max_length=2,
        choices=Status.choices,
        default=Status.FREELANCER_CANDIDATE,
    )
    founder = models.BooleanField(
        default=False, verbose_name=_("Основатель"), blank=True
    )
    slug = models.SlugField(max_length=155, unique=True, blank=True)
    referal_link = models.CharField(_("реферальная ссылка"), max_length=150, blank=True)

    rub_acc = models.OneToOneField(
        verbose_name=_("Счет RUB"),
        to="accounts.Account",
        on_delete=models.CASCADE,
        related_name="rub_acc",
        blank=True,
    )
    usd_acc = models.OneToOneField(
        verbose_name=_("Счет USD"),
        to="accounts.Account",
        on_delete=models.CASCADE,
        related_name="usd_acc",
        blank=True,
    )
    eur_acc = models.OneToOneField(
        verbose_name=_("Счет EUR"),
        to="accounts.Account",
        on_delete=models.CASCADE,
        related_name="eur_acc",
        blank=True,
    )

    legal_status = models.CharField(
        _("юридический статус"),
        max_length=2,
        choices=LegalStatus.choices,
        default=LegalStatus.PHYSICAL,
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    username_validator = UnicodeUsernameValidator()

    objects = CustomUserManager()

    class MPTTMeta:
        user_insertion_by = ["email"]

    class Meta:
        ordering = ("date_joined",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    def __str__(self) -> str:
        return self.email

    @property
    def referals(self):
        """Получение рефералов"""
        level1 = CustomUser.objects.filter(parent=self)
        level2 = CustomUser.objects.filter(parent__in=level1)
        level3 = CustomUser.objects.filter(parent__in=level2)
        return {"level1": level1, "level2": level2, "level3": level3}

    def get_referal_link(self):
        """Формирование реф.ссылки, после оплаты вступительного взноса"""
        from .services import CustomnUserService
        self.referal_link = CustomnUserService.get_referal_link(user=self)
        return self.referal_link

    def _create_accounts(self):
        """Формирование счетов юзера"""
        self.rub_acc = Account.objects.create(account_name=f"{generate_account_number()}R")
        self.usd_acc = Account.objects.create(account_name=f"{generate_account_number()}U", currency="USD")
        self.eur_acc = Account.objects.create(account_name=f"{generate_account_number()}E", currency="EUR")

    def _update_fund_acc_and_user_acc(self, currency):
        """получение счетов фонда и их пополнение вступительным взносом"""
        fund = Fund.objects.get(pk=1)
        no_demand_fund = Fund.objects.get(pk=2)
        match currency:
            case "RUB":
                acc = self.rub_acc
                transfer_money(
                    acc, fund.rub_account, 999, currency=currency, purpose="DF"
                )
            case "USD":
                acc = self.usd_acc
                transfer_money(
                    acc, fund.usd_account, 15, currency=currency, purpose="DF"
                )
            case "EUR":
                acc = self.eur_acc
                transfer_money(
                    acc, fund.eur_account, 15, currency=currency, purpose="DF"
                )
        return fund, no_demand_fund, acc

    def _update_balance(self, acc, currency):
        """Пополнение баланса юзера"""
        match currency:
            case 'RUB':
                acc.balance += 2000
            case 'USD':
                acc.balance += 30
            case 'EUR':
                acc.balance += 30
        acc.save()
        
    def money_transfer_to_fund_parent(self, currency):
        father = self.parent
        grandfather = None
        grand_grandfather = None
        if father:
            grandfather = father.parent
            if grandfather:
                grand_grandfather = grandfather.parent
        match currency:
            case "RUB":
                self._update_balance(self.rub_acc, currency)
                fund, no_demand_fund, rub_acc = self._update_fund_acc_and_user_acc(
                    currency=currency
                )
                if father:
                    transfer_money(
                        rub_acc,
                        father.rub_acc,
                        amount_father_rub,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        rub_acc,
                        no_demand_fund.rub_account,
                        amount_father_rub,
                        currency,
                        purpose="ND",
                    )
                if grandfather:
                    transfer_money(
                        rub_acc,
                        grandfather.rub_acc,
                        grandfather_amount_rub,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        rub_acc,
                        no_demand_fund.rub_account,
                        grandfather_amount_rub,
                        currency,
                        purpose="ND",
                    )
                if grand_grandfather:
                    transfer_money(
                        rub_acc,
                        grand_grandfather.rub_acc,
                        grand_grandfather_amount_rub,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        rub_acc,
                        no_demand_fund.rub_account,
                        grand_grandfather_amount_rub,
                        currency,
                        purpose="ND",
                    )
                if self.status == "FC":
                    self.status = CustomUser.Status.FREELANCER
                if self.status == "CC":
                    self.status = CustomUser.Status.CUSTOMER
                self.referal_link = self.get_referal_link()
                self.paid_entrance_rub = True

            case "USD":
                self._update_balance(self.usd_acc, currency)
                fund, no_demand_fund, usd_acc = self._update_fund_acc_and_user_acc(
                    currency=currency
                )
                if father:
                    transfer_money(
                        usd_acc,
                        father.usd_acc,
                        amount_father_usd,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        usd_acc,
                        no_demand_fund.usd_account,
                        amount_father_usd,
                        currency,
                        purpose="ND",
                    )
                if grandfather:
                    transfer_money(
                        usd_acc,
                        grandfather.usd_acc,
                        grandfather_amount_usd,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        usd_acc,
                        no_demand_fund.usd_account,
                        grandfather_amount_usd,
                        currency,
                        purpose="ND",
                    )
                if grand_grandfather:
                    transfer_money(
                        usd_acc,
                        grand_grandfather.usd_acc,
                        grand_grandfather_amount_usd,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        usd_acc,
                        no_demand_fund.usd_account,
                        grand_grandfather_amount_usd,
                        currency,
                        purpose="ND",
                    )
                if self.status == "FC":
                    self.status = CustomUser.Status.FREELANCER
                if self.status == "CC":
                    self.status = CustomUser.Status.CUSTOMER
                self.referal_link = self.get_referal_link()
                self.paid_entrance_usd = True

            case "EUR":
                self._update_balance(self.eur_acc, currency)
                fund, no_demand_fund, eur_acc = self._update_fund_acc_and_user_acc(
                    currency=currency
                )
                if father:
                    transfer_money(
                        eur_acc,
                        father.eur_acc,
                        amount_father_usd,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        eur_acc,
                        no_demand_fund.eur_account,
                        amount_father_usd,
                        currency,
                        purpose="ND",
                    )
                if grandfather:
                    transfer_money(
                        eur_acc,
                        grandfather.eur_acc,
                        grandfather_amount_usd,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        eur_acc,
                        no_demand_fund.eur_account,
                        grandfather_amount_usd,
                        currency,
                        purpose="ND",
                    )
                if grand_grandfather:
                    transfer_money(
                        eur_acc,
                        grand_grandfather.eur_acc,
                        grand_grandfather_amount_usd,
                        currency,
                        purpose="RF",
                    )
                else:
                    transfer_money(
                        eur_acc,
                        no_demand_fund.eur_account,
                        grand_grandfather_amount_usd,
                        currency,
                        purpose="ND",
                    )
                if self.status == "FC":
                    self.status = CustomUser.Status.FREELANCER
                if self.status == "CC":
                    self.status = CustomUser.Status.CUSTOMER
                self.referal_link = self.get_referal_link()
                self.paid_entrance_eur = True

    def save(self, *args, **kwargs):
        """Формирование счетов при регистрации, подвтерждение оплаты вступительного взноса,
        списание денег от вступительного взноса по фондам и реферов"""
        from .services import CustomnUserService
        if self.pk:
            original_instance = CustomUser.objects.get(pk=self.pk)
            if self.paid_entrance_rub != original_instance.paid_entrance_rub and self.paid_entrance_rub:
                self.money_transfer_to_fund_parent('RUB')
            if self.paid_entrance_usd != original_instance.paid_entrance_usd and self.paid_entrance_usd:
                self.money_transfer_to_fund_parent('USD')
            if self.paid_entrance_eur != original_instance.paid_entrance_eur and self.paid_entrance_eur:
                self.money_transfer_to_fund_parent('EUR')

        elif not self.pk:
            self._create_accounts()
       
        if not self._state.adding:
            username_slug = CustomnUserService.get_username_slug(username=self.username)
            if self.slug != username_slug:
                self.slug = username_slug
        super().save(*args, **kwargs)


class UserInfoCompany(models.Model):
    employee_position = models.CharField(max_length=100,
                                         verbose_name=_("Должность представитля"))
    company_name = models.CharField(max_length=100,
                                    verbose_name=_('Полное название компании'),
                                    db_index=True)
    short_company_name = models.CharField(max_length=100,
                                          verbose_name=_('Короткое название компании'))
    ceo_name = models.CharField(max_length=150,
                                verbose_name=_('ФИО руководителя'))
    ceo_post = models.CharField(verbose_name=_('Должность руководителя'),
                                max_length=100, blank=True, null=True)
    adress_in_law = models.CharField(verbose_name=_('Юр. адрес'),
                                     max_length=200)
    adress_fact = models.CharField(verbose_name=_('Физ. адрес'),
                                   max_length=200)
    reg_number = models.CharField(verbose_name=_('ОГРН'),
                                  max_length=50)
    company_number = models.CharField(verbose_name=_('ИНН'),
                                      max_length=30, blank=True,
                                      null=True)
    kpp_number = models.CharField(verbose_name=_('КПП'),
                                  max_length=30,
                                  blank=True, null=True)
    certificate = models.CharField(max_length=30,
                                   verbose_name=_('Свидетельство номер'),
                                   blank=True, null=True)
    certificate_file = models.FileField(verbose_name=_('Свидетельство файл'),
                                        upload_to='company_docs/%Y/%m/%d')
    company_site = models.CharField(verbose_name=_('Сайт компании'),
                                    max_length=80, blank=True,
                                    null=True)
    company_phone = models.CharField(verbose_name=_('Телефон компании'),
                                     max_length=30)
    company_email = models.CharField(verbose_name=_('Email компании'),
                                     max_length=50)
    social_site = models.CharField(verbose_name=_('Социальные сети'),
                                   max_length=80, blank=True,
                                   null=True)


    class Meta:
        verbose_name = _("Компания Пользователя")
        verbose_name_plural = _("Компании Пользователей")

    def __str__(self) -> str:
        return self.company_name


class UserInfo(models.Model):
    """Информация по юзеру"""
    USER_CURRENCY_CHOICES = (
        ("USD", _("$")),
        ("RUB", _("Р")),
        ("EUR", _("€")),
    )

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user_info"
    )

    first_name = models.CharField(max_length=155,
                                  verbose_name=_('Имя'))
    last_name = models.CharField(max_length=155,
                                 verbose_name=_('Фамилия'),
                                 db_index=True)
    experience = models.CharField(
        max_length=20,
        verbose_name='Стаж:',
        blank=True, null=True
    )
    father_name = models.CharField(max_length=155, blank=True, null=True,
                                   verbose_name=_('Отчество'))
    date_of_birth = models.DateField(verbose_name=_('Дата рождения'))

    phone_number = models.CharField(max_length=30,
                                    verbose_name=_('Номер телефона'))
    avatar = models.ImageField(upload_to='users/avatar/%Y/%m/%d',
                               blank=True, null=True,
                               verbose_name=_('Аватар'))
    on_vacation = models.BooleanField(default=False,
                                      verbose_name=_('Отпуск'))
    adress = models.CharField(max_length=200,
                              verbose_name=_('Адрес проживания'))
    skill = models.TextField(verbose_name=_("Навыки"),
                             blank=True, null=True)
    review_ratio = models.DecimalField(max_digits=5, decimal_places=2,
                                       default=0, blank=True, null=True,
                                       verbose_name=_("Звездность"))
    cost_of_hour_work = models.DecimalField(max_digits=10, decimal_places=2,
                                            verbose_name=_("Стоимость часа работы"),
                                            blank=True, null=True)
    currency = models.CharField(max_length=3, choices=USER_CURRENCY_CHOICES, null=True,
                                blank=True, verbose_name=_('Валюта стоимости часа работ'))
    profile_description = models.TextField(max_length=1000,
                                           verbose_name=_("Описание профиля"),
                                           blank=True, null=True)
    baner = models.FileField(upload_to='users/baners/%Y/%m/%d',
                             verbose_name=_("Банер"),
                             blank=True, null=True)

    polzunok = models.BooleanField(default=False)

    company = models.ForeignKey(UserInfoCompany, on_delete=models.PROTECT,
                                related_name='companies', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT,
                                related_name='user_countries')
    specialization = models.ManyToManyField(Specialization, through='UserSpecialization')


    def update_review_ratio(self):
        postive_review = Review.objects.filter(
            order__executor=self.user, status=Review.Status.POSITIVE
        ).count()
        negative_review = Review.objects.filter(
            order_executor=self.user, status=Review.Status.NEGATIVE
        ).count()
        if postive_review + negative_review > 0:
            ratio = postive_review / (negative_review + postive_review) * 100
            self.review_ratio = ratio
            self.save()

    class Meta:
        verbose_name = _("Данные пользователя")
        verbose_name_plural = _("Данные пользователей")

    def __str__(self):
        return self.first_name or self.user.pk



class UserSpecialization(models.Model):
    user = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name="user_specializations"
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name="user_specializations",
        null=True,
        blank=True,
    )
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Специализация юзера"
        verbose_name_plural = "Специализации юзера"

    def get_user(self):
        return self.user.user.email

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.specialization.name}"


class EmailToken(models.Model):
    """Модель Токенов Email"""

    PURPOSE_CHOICE = [
        ("confirm", "Подтверждение регистрации"),
        ("email", "Смена email"),
        ("reset_link", "Ссылка сброса пароля"),
        ("reset", "Сброс пароля"),
    ]
    user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Пользователь, связанный с токеном"),
        on_delete=models.CASCADE,
        related_name="email_token",
    )
    created_at = models.DateTimeField(_("Дата генерации"), auto_now_add=True)
    key = models.CharField(
        max_length=50, verbose_name=_("Токен"), db_index=True, unique=True
    )
    purpose = models.CharField(
        verbose_name=_("Назначение"),
        max_length=10,
        choices=PURPOSE_CHOICE,
        default="confirm",
    )
    number_of_checks = models.PositiveSmallIntegerField(
        _("Number of checks"), default=0
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(EmailToken, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return get_token_generator().generate_token()

    class Meta:
        verbose_name = "Токен Email"
        verbose_name_plural = "Токены Email"
        db_table = "EmailToken"

    def __str__(self) -> str:
        return f"Токен email для пользователя {self.user}"
