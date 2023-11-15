from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from typing import Dict, Union

from app.main_users.models import CustomUser
from app.chat.models import Thread, Comment, ChatRoom, Messages

class ChatUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user_info.first_name')
    last_name = serializers.CharField(source='user_info.last_name')

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name'
        )



class ThreadSerializer(serializers.ModelSerializer):
    creator = ChatUserSerializer(read_only=True)
    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'text',
            'creator',
            'created_at'
        )
        read_only_fields = (
            'created_at', 'id'
        )


class CommentSerializer(serializers.ModelSerializer):
    commentator = ChatUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = (
            'thread',
            'text',
            'comment',
            'commentator',
            'created_at',
        )
        read_only_fields = (
            'created_at', 'thread'
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = (
            'sender',
            'message',
            'created_at',
            'room'
        )
        read_only_fields = ('created_at', 'sender', 'room')


class ChatSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    user_1 = ChatUserSerializer(read_only=True)
    user_2 = ChatUserSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = (
            'id',
            'name',
            'user_1',
            'user_2',
            'created_at',
            'messages',
        )
        read_only_fields = (
            'created_at', 'name'
        )

    def get_messages(self, instance) -> Dict[str, Union[Dict, str]]:
        try:
            return MessageSerializer(instance.messages, many=True, read_only=True).data
        except AttributeError:
            return {'error': 'No messages found yet.'}
