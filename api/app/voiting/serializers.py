from rest_framework import serializers
from django.db.models import Sum
from .models import Question, Voite

        
class VoiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voite
        fields = ['id', 'positive_voice', 'negative_voice', 'abstaned_voice', 'user']
        read_only_fields = ['user',]

        
        
class QuestionVoiteSerializer(serializers.ModelSerializer):
    voites = VoiteSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'pub_date', 'voites']
        read_only_fields = ['pub_date', 'voites']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        voiting_data = validated_data.pop('voites')
        question = super().update(instance, validated_data)
        for voite_param in voiting_data:
            voite = Voite.objects.create(question=question, **voite_param, user=self.context['request'].user)
        return question
        
