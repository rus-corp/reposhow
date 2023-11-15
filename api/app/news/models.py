from django.db import models
from django.utils.translation import gettext_lazy as _

from app.main_users.models import CustomUser


class News(models.Model):
    """Новости"""

    title = models.CharField(max_length=150, verbose_name=_("заголовок"))
    text = models.TextField(max_length=1500, verbose_name=_("текст"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("дата создания"))
    for_all = models.BooleanField(verbose_name=_("для всех"), default=False)
    for_freelancers = models.BooleanField(
        verbose_name=_("для фриласнеров"), default=False
    )
    for_customers = models.BooleanField(verbose_name=_("для заказчиков"), default=False)
    for_founders = models.BooleanField(verbose_name=_("для основателей"), default=False)
    slug = models.SlugField(max_length=255, unique_for_date="created")

    class Meta:
        ordering = ("-created",)
        verbose_name = _("новость")
        verbose_name_plural = _("новости")

        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return self.title


class UserViews(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userviews", verbose_name=_("User"))
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, blank=True, null=True, related_name="newsviews", verbose_name=_("News")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("дата создания"))


    def __str__(self) -> str:
        return str(self.user.username)

    class Meta:
        db_table = "user_viewed"
        verbose_name = _("Просмотры")
        verbose_name_plural = _("Просмотры")
        ordering = ("-created",)