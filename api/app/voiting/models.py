from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class QuestionManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(question_status=Question.QuestionStatus.ACTUAL)
        )


class Question(models.Model):
    class QuestionStatus(models.TextChoices):
        ACTUAL = "AC", "Actual"
        ARCHIVE = "AR", "Archive"

    text = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    question_status = models.CharField(
        verbose_name=_("Статус вопроса"),
        max_length=2,
        choices=QuestionStatus.choices,
        default=QuestionStatus.ACTUAL,
    )

    objects = models.Manager()
    actual = QuestionManager()

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    def __str__(self):
        return self.text


class Voite(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="voites"
    )
    positive_voice = models.IntegerField(_("ЗА"), default=0, blank=True)
    negative_voice = models.IntegerField(_("Против"), default=0, blank=True)
    abstaned_voice = models.IntegerField(_("Воздержалось"), default=0, blank=True)
    user = models.ForeignKey(
        to="main_users.CustomUser", on_delete=models.PROTECT, related_name="voites"
    )

    class Meta:
        verbose_name = _("Голос")
        verbose_name_plural = _("Голосы")
        unique_together = ["question", "user"]
