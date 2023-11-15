from django.contrib import admin


from .models import Theme, Question, Answer

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    

@admin.register(Question)
class QusetionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'theme']
    
    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'question']