from rest_framework import serializers


from .models import Theme, Question, Answer


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name',]
        

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'name',]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    theme = ThemeSerializer()
    class Meta:
        model = Question
        fields = ['id', 'name', 'answers','theme']
        



        




        