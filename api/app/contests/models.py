from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import TreeForeignKey

from app.main_users.models import CustomUser


class Contest(models.Model):
    name = models.CharField(verbose_name=_("Название конкурса"), max_length=155, db_index=True)
    desc = models.TextField(verbose_name=_("Описание конкурса"), max_length=1000, blank=True, null=True)
    price = models.DecimalField(verbose_name=_("Цена конкурса"), max_digits=10, decimal_places=2, default=0)
    period = models.DateField(verbose_name=_("Срок риема работ"))
    created_at = models.DateTimeField(verbose_name=_("Дата создания конкурса"), auto_now_add=True)
    completion_date = models.DateField(verbose_name=_("Дата выбора победителя"), )
    slug = models.SlugField(max_length=120, unique_for_date='created_at')
    views = models.IntegerField(default=0)
    target_audience = models.TextField(_('Целевая аудитория'), blank=True, max_length=300)
    atention = models.TextField(_('Обратить внимание'), max_length=300, blank=True)

    activity = models.ForeignKey(to='categories.Activity', verbose_name=_("Сфера деятельности"), on_delete=models.CASCADE, related_name='contest_activities')
    category = models.ForeignKey(to='categories.Category', verbose_name=_("Категория"), on_delete=models.CASCADE, related_name='contest_categories')
    specialization = models.ForeignKey(to='categories.Specialization', verbose_name=_("Специализация"), on_delete=models.CASCADE, related_name='contest_specializations')

    customer = models.ForeignKey(CustomUser, verbose_name=_("Заказчик"), on_delete=models.CASCADE, related_name='contest_customers')
    executor = models.ManyToManyField(CustomUser, through='ContestResponse', verbose_name=_("Исполнители"), blank=True)

    rub_acc = models.OneToOneField(to='accounts.Account', on_delete=models.CASCADE, related_name='contest_rub_acc')
    usd_acc = models.OneToOneField(to='accounts.Account', on_delete=models.CASCADE, related_name='contest_usd_acc')
    eur_acc = models.OneToOneField(to='accounts.Account', on_delete=models.CASCADE, related_name='contest_eur_acc')

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'

    def __str__(self) -> str:
        return self.name


class ContestAppFiles(models.Model):
    file = models.FileField(upload_to='contets_files/%Y/%m%d', verbose_name=_(""))
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='contest_files', verbose_name=_(""))

    class Meta:
        verbose_name = 'Файл кокурса'
        verbose_name_plural = 'Файлы конкурса'

    def __str__(self) -> str:
        return self.contest.name


class ContestResponse(models.Model):
    class ExecutorStatus(models.TextChoices):
        NO_STATUS = 'NS', 'No_Status'
        CANDIDATE = 'CN', 'Candidate'
        EXECUTOR = 'EX', 'Executor'

    class ExecutorPlace(models.TextChoices):
        NO_PLACE = 'NP', 'No_place'
        FIRST_PLACE = 'FP', 'First_place'
        SECOND_PLACE = 'SC', 'Second_place'
        THIRD_PLACE = 'TP', 'Third_place'
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='contest_responses', verbose_name=_(""))
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='contest_responses', verbose_name=_(""))
    executor_status = models.CharField(max_length=2, choices=ExecutorStatus.choices, default=ExecutorStatus.NO_STATUS, verbose_name=_(""))
    executor_place = models.CharField(max_length=2, choices=ExecutorPlace.choices, default=ExecutorPlace.NO_PLACE, verbose_name=_(""))
    desc = models.TextField(max_length=500, blank=True, null=True, verbose_name=_(""))
    created_at = models.DateField(auto_now_add=True, verbose_name=_(""))
    file1 = models.FileField(upload_to='contest_files/responses/%Y/%m/%d', blank=True, null=True, verbose_name=_(""))
    file2 = models.FileField(upload_to='contest_files/responses/%Y/%m/%d', blank=True, null=True, verbose_name=_(""))
    file3 = models.FileField(upload_to='contest_files/responses/%Y/%m/%d', blank=True, null=True, verbose_name=_(""))

    class Meta:
        verbose_name = 'Отклик на конкурс'
        verbose_name_plural = 'Отклики на конкурсы'

    def __str__(self) -> str:
        return f'{self.contest.name} - {self.executor.username}'


class ContestResponseComment(models.Model):
    text = models.TextField(max_length=500, verbose_name=_(""))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(""))

    contest_response = models.ForeignKey(ContestResponse, on_delete=models.CASCADE ,related_name='contest_response_comments', verbose_name=_(""))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contest_response_comments', verbose_name=_(""))
    parent = TreeForeignKey('self', on_delete=models.PROTECT, related_name='contest_replies', blank=True, null=True, verbose_name=_(""))

    file1 = models.FileField(upload_to='contest_response_comments/%Y/%m/%d', blank=True, null=True, verbose_name=_(""))
    file2 = models.FileField(upload_to='contest_response_comments/%Y/%m/%d', blank=True, null=True, verbose_name=_(""))
    file3 = models.FileField(upload_to='contest_response_comments/%Y/%m/%d', blank=True, null=True, verbose_name=_(""))

    class Meta:
        verbose_name = 'Комметрий отклика'
        verbose_name_plural = 'Комментарии отклика'

    def __str__(self) -> str:
        return self.contest_response.pk
