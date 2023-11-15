from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer



class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        theme_id = self.request.query_params.get('theme')
        if theme_id:
            return Question.objects.filter(theme=theme_id)
        return Question.objects.all()


