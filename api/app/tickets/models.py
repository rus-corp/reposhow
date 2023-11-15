from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

class Ticket(MPTTModel):
    name = models.CharField(max_length=300, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = _('Тикет')
        verbose_name_plural = _('Тикеты')


    def __str__(self) -> str:
        return self.name