from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from app.portfolio.validators import file_size_validate



class Company_Doc(models.Model):
    """Документы и договора компании"""
    name = models.CharField(max_length=155)
    desc = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/', blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_private = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Документ компании'
        verbose_name_plural = 'Документы компании'
        
        
    def __str__(self) -> str:
        return self.name
        
        
        
class ReferalLink(models.Model):
    image_validator = FileExtensionValidator(allowed_extensions=['png', 'jpeg'],
                                             message=_('Ошибка загрузки: допускаются только файлы с расширением .jpg .png'))
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    specialization = models.CharField(max_length=100)
    work_links = models.TextField(max_length=400, blank=True)
    file1 = models.FileField(upload_to='get_referal_link/%Y/%m/%d', validators=[file_size_validate], blank=True, null=True)
    file2 = models.FileField(upload_to='get_referal_link/%Y/%m/%d', validators=[file_size_validate], blank=True, null=True)
    file3 = models.FileField(upload_to='get_referal_link/%Y/%m/%d', validators=[file_size_validate], blank=True, null=True)
    file4 = models.FileField(upload_to='get_referal_link/%Y/%m/%d', validators=[file_size_validate], blank=True, null=True)
    file5 = models.FileField(upload_to='get_referal_link/%Y/%m/%d', validators=[file_size_validate], blank=True, null=True)
    
    
    class Meta:
        verbose_name = 'Получатель реф ссылки'
        verbose_name_plural = 'Получатели реф ссылки'
    
    
    def __str__(self) -> str:
        return self.email