from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets



from .models import Activity, Category, Specialization
from .serializers import ActivitySerializer, CategorySerializer, SpecializationSerializer



class ActivityApiView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class CategApiView(generics.ListAPIView):
    queryset = Category.objects.none()
    serializer_class = CategorySerializer

    def get(self, request, activity):
        try:
            activity = Activity.objects.get(slug=activity)
        except Activity.DoesNotExist:
            return Response({'error': False})

        categories = Category.objects.filter(activity=activity)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



class SpecializationApiView(generics.ListAPIView):
    queryset = Specialization.objects.none()
    serializer_class = SpecializationSerializer

    def get(self, request, categories):
        try:
            categories = Category.objects.get(slug=categories)
        except Category.DoesNotExist:
            return Response({'status':False})

        specialization = Specialization.objects.filter(category=categories)
        serializer = SpecializationSerializer(specialization, many=True)
        return Response(serializer.data)



