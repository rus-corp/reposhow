from rest_framework import serializers

from .models import News

class NewsSerializer(serializers.ModelSerializer):
    is_read = serializers.BooleanField(read_only=True)
    class Meta:
        model = News
        fields = ['id', 'title', 'text', 'created', 'is_read']
        
class ViewNewsSerializer(serializers.Serializer):
    news_id = serializers.ListField(child=serializers.IntegerField())