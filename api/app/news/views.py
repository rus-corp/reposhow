from django.db.models import  Exists, OuterRef
from rest_framework import viewsets, response
from drf_spectacular.utils import extend_schema

from .models import News, UserViews
from .serializers import NewsSerializer, ViewNewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ("get", "list", "post")

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.status == "FR":
                news = News.objects.filter(for_freelancers=True)
            elif user.status == "CC":
                news = News.objects.filter(for_customers=True)
            elif user.founder:
                news = News.objects.filter(for_founders=True)
            else:
                news = News.objects.filter(for_all=True) 
            queryset = news.annotate(
                is_read=Exists(
                    UserViews.objects.filter(user=user, news=OuterRef("id"))
                ),
            ).order_by("-is_read")
        else:
            queryset = News.objects.filter(for_all=True) 
        return queryset.distinct()
    
    @extend_schema(request=ViewNewsSerializer)
    def create(self, request):
        serializer = ViewNewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news_ids = serializer.validated_data.get("news_id")
        for news_id in news_ids:
            try:
                news = News.objects.get(id=news_id)
                views = UserViews.objects.filter(user=request.user, news=news)
                if not views.exists():
                    UserViews.objects.create(
                        user=request.user,
                        news=news
                    )
            except News.DoesNotExist:
                pass
        return response.Response(data={"message": f"News marked is_read"}, status=201)
