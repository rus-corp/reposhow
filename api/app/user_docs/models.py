from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from .validators import document_size_validate



class UserDoc(models.Model):
    """Личные документы юзера"""

    document_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'pdf'],
        message=_('Ошибка загрузки: допускаются только файлы с расширением .jpg .pdf .png'))
    personal_number = models.CharField(_('ИНН или персональный номер'), max_length=17, blank=True, null=True, db_index=True)
    document = models.FileField(_('документ'), upload_to='documents/%Y/%m/%d',
                                blank=True, validators=[document_validator, document_size_validate])
    document_name = models.CharField(_("Название документа",), max_length=100)
    document_number = models.CharField(_('Серия или номер документа'), max_length=55, blank=True, db_index=True)
    document_issued = models.CharField(_('Когда и кем выдан'), max_length=255)


    user = models.OneToOneField(to='main_users.CustomUser', on_delete=models.CASCADE, related_name='user_docs')

    def get_user(self):
        return self.user.email

    class Meta:
        verbose_name = 'Документ юзера'
        verbose_name_plural = 'Документы юзера'



class BankAccount(models.Model):
    """Информация по банку юзера, куда будут выводиться деньги"""
    bank_name = models.CharField(_('Наименование банка'), max_length=255, null=True, blank=True)
    bank_address = models.CharField(_('Адрес банка'), max_length=255, null=True, blank=True)
    bank_bic = models.CharField(_('БИК банка'), max_length=55, blank=True, null=True)
    bank_correspondent_account = models.CharField(_('Корреспондентский счет банка'), max_length=55, blank=True, null=True)
    payment_account = models.CharField(_('Расчетный счет'), max_length=55, blank=True, null=True)
    recipients_name = models.CharField(_('Имя получателя платежа'), max_length=255, blank=True)
    user = models.ForeignKey(to='main_users.CustomUser', on_delete=models.CASCADE, related_name='user_bank')

    def get_user(self):
        return self.user.email

    class Meta:
        verbose_name = 'Реквизит банка'
        verbose_name_plural = 'Реквизиты банка'




class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=150, unique=True)
    phone_code = models.CharField(max_length=15, blank=True, null=True)
    flag = models.FileField(upload_to='flags/', null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='countries')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self) -> str:
        return self.name



class Contract(models.Model):
    user = models.OneToOneField(to='main_users.CustomUser', on_delete=models.CASCADE, related_name='contracts')
    text = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Договор юзера'
        verbose_name_plural = 'Договоры юзеров'
        
    def __str__(self) -> str:
        return self.user.email