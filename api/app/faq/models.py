from django.db import models
from django.utils.translation import gettext_lazy as _



class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


    def __str__(self):
        return self.name
    
    
    
class Question(models.Model):
    name = models.CharField(max_length=200, unique=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='questions')
    
    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
            
    def __str__(self) -> str:
        return self.name
    
    
    

class Answer(models.Model):
    name = models.TextField(max_length=1000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    
    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')
        
    def __str__(self) -> str:
        return self.name
    
    