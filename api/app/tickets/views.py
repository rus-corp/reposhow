from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(ReadOnlyModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    
