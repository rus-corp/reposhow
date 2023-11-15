from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class ReferalLinkResponse(models.Model):
    """Класс зранящий в себе реферальную ссылку."""
    referal_link = models.CharField(
        'Ссылка:',
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Владелец ссылки:'
    )

    class Meta:
        verbose_name = 'Реферальная ссылка'
        verbose_name_plural = 'Реферальные ссылки'

    def save(self, *args, **kwargs):
        if not self.pk and ReferalLinkResponse.objects.exists():
            # if you'll not check for self.pk
            # then error will also be raised in the update of exists model
            raise ValidationError('There is can be only one ReferalLink instance')
        return super(ReferalLinkResponse, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
