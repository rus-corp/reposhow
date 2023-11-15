from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import file_size_validate
from app.orders.models import Order

User = get_user_model()


class Work(models.Model):
    """Портфолио"""
    CURRENCY_CHOICES = (
        ("USD", _("$")),
        ("RUB", _("Р")),
        ("EUR", _("€")),
    )
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg'],
        message=_('Ошибка загрузки: допускаются только файлы с расширением .jpg .png')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('пользователь'), related_name='works')

    title = models.CharField(max_length=255, verbose_name=_('заголовок'), db_index=True)
    description = models.TextField(verbose_name=_('описание'))
    image = models.ImageField(upload_to='portfolio/covers/%Y/%m/%d/', null=True, blank=True, validators=[image_validator, file_size_validate], verbose_name=_('обложка'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    corrected_at = models.DateTimeField(auto_now=True, verbose_name=_('дата изменения'))
    price = models.DecimalField(_('стоимость'), default=0, max_digits=18, decimal_places=2, null=True, blank=True)
    price_currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, verbose_name=_('валюта'), null=True, blank=True)
    link = models.CharField(max_length=255, verbose_name=_('ссылка'), null=True, blank=True)
    video = models.CharField(max_length=255, verbose_name=_('видео'), null=True, blank=True)
    table_place = models.IntegerField(default=1, verbose_name=_('Место в таблице'), validators=[MinValueValidator(1)])
    time_spend = models.IntegerField(default=1, blank=True, null=True, verbose_name=_('Потраченное время в часах'), validators=[MinValueValidator(1)])
    file1 = models.FileField(upload_to='portfolio/files/%Y/%m/%d/', verbose_name=_('файл1'), validators=[file_size_validate], null=True, blank=True)
    file2 = models.FileField(upload_to='portfolio/files/%Y/%m/%d/', verbose_name=_('файл2'), validators=[file_size_validate], null=True, blank=True)
    file3 = models.FileField(upload_to='portfolio/files/%Y/%m/%d/', verbose_name=_('файл3'), validators=[file_size_validate], null=True, blank=True)
    file4 = models.FileField(upload_to='portfolio/files/%Y/%m/%d/', verbose_name=_('файл4'), validators=[file_size_validate], null=True, blank=True)
    category = models.ForeignKey(to='categories.Specialization', verbose_name=_('категория'), on_delete=models.SET_NULL, null=True, related_name='works')
    is_active = models.BooleanField(default=True, verbose_name=_('отображать на сайте'), db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('работа')
        verbose_name_plural = _('работы')
        ordering = ['-created_at']


class CurrentWork(Work):
    order = models.ForeignKey(Order, verbose_name=("выполненный заказ"), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('текущая работа')
        verbose_name_plural = _('текущие работы')
        ordering = ['-created_at']
