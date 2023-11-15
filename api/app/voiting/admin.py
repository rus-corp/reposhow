from django.contrib import admin
from django.db.models import Sum
from .models import Question, Voite


class VoiteInline(admin.TabularInline):
    model = Voite
    extra = 1
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'num_positive_votes', 'num_negative_votes', 'num_abstaned_votes', 'pub_date', 'question_status']
    inlines = [VoiteInline,]
    
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            num_positive_votes=Sum('voites__positive_voice'),
            num_negative_votes=Sum('voites__negative_voice'),
            num_abstaned_votes=Sum('voites__abstaned_voice')
        )
        return queryset
    
    def num_positive_votes(self, obj):
        return obj.num_positive_votes
    num_positive_votes.short_description = 'ЗА'
    
    def num_negative_votes(self, obj):
        return obj.num_negative_votes
    num_negative_votes.short_description = 'ПРОТИВ'
    
    def num_abstaned_votes(self, obj):
        return obj.num_abstaned_votes
    num_abstaned_votes.short_description = 'Воздержалось'



@admin.register(Voite)
class VoiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'positive_voice', 'negative_voice', 'abstaned_voice']
