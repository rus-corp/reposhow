from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def avatar_size_validate(value):
    """ Валидатор. Проверяет размер загружаемого изображения """
    image_size = value.size
    max_megabytes = 2.0
    if image_size > max_megabytes * 1024 * 1024:
        raise ValidationError(_(f"Ошибка загрузки: допускается размер файла не более {max_megabytes} MB"))


def document_size_validate(value):
    """ Валидатор. Проверяет размер загружаемого документа """
    document_size = value.size
    max_megabytes = 5.0
    if document_size > max_megabytes * 1024 * 1024:
        raise ValidationError(_(f"Ошибка загрузки: допускается размер файла не более {max_megabytes} MB"))