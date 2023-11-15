from rest_framework import viewsets
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta

from app.main_users.permissions import IsFreelancerOrCustomerOrReadOnly
from .models import Question
from .serializers import QuestionVoiteSerializer


class VoiteViewSet(viewsets.ModelViewSet):
    queryset = Question.actual.all()
    serializer_class = QuestionVoiteSerializer
    permission_classes = [permissions.IsAuthenticated, 
                          IsFreelancerOrCustomerOrReadOnly]
    
    def get_queryset(self):
        three_weeks = timezone.now() - timedelta(weeks=3)
        return Question.objects.filter(pub_date__gte=three_weeks)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    


