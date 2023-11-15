from django.contrib.auth import get_user_model
from django.db import models
from mptt.fields import TreeForeignKey

from app.portfolio.validators import file_size_validate


User = get_user_model()


class Thread(models.Model):
    """Таблица обсуждений."""

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="threads",
        verbose_name="Создатель:",
    )
    title = models.CharField("Тема:", max_length=150)
    text = models.CharField(
        "Текст обсуждения:",
        max_length=400,
    )
    created_at = models.DateTimeField("Время создания треда:", auto_now_add=True)

    class Meta:
        verbose_name = "Тред"
        verbose_name_plural = "Треды"

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Таблица комментариев к тредам."""

    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments", verbose_name="Тред:"
    )
    commentator = models.ForeignKey(
        User,
        related_name="comments",
        verbose_name="Комментатор:",
        on_delete=models.DO_NOTHING,
    )
    comment = TreeForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=("Главный комментарий:"),
        related_name="comments",
    )
    text = models.CharField(
        "Текст комментария:",
        max_length=400,
    )
    created_at = models.DateTimeField("Время создания комментария:", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return self.thread.title + " " + self.commentator.username


class ChatRoom(models.Model):
    """Таблица чат комнат."""

    name = models.CharField(
        "Название чат комнаты:",
        max_length=150,
    )
    user_1 = models.ForeignKey(
        User, models.CASCADE, related_name="chat_room_1", verbose_name="Пользователь 1:"
    )
    user_2 = models.ForeignKey(
        User, models.CASCADE, related_name="chat_room_2", verbose_name="Пользователь 2:"
    )
    created_at = models.DateTimeField("Время создания комнаты:", auto_now_add=True)

    class Meta:
        verbose_name = "Чат комната"
        verbose_name_plural = "Чат комнаты"
        unique_together = ("user_1", "user_2")

    def __str__(self) -> str:
        return self.name


def room_name(instance, filename):
    return 'messages/files/{0}/{1}'.format(instance.room.name, filename)


class Messages(models.Model):
    """Таблица сообщений в чат комнате."""
    room = models.ForeignKey(
        ChatRoom, models.CASCADE, related_name="messages", verbose_name="Комната:"
    )
    message = models.CharField(
        "Текст сообщения:",
        max_length=600,
    )
    sender = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="messages",
    )
    file = models.FileField(
        upload_to=room_name,
        verbose_name="файл",
        validators=[file_size_validate],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Дата отправки сообщения:", auto_now_add=True)

    def __str__(self) -> str:
        return self.room.name
