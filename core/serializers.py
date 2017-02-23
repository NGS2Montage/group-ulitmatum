from django.contrib.auth.models import User

from rest_framework import serializers

from .models import ChatMessage, Friend


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')
        read_only_fields = ('pk', 'username')


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ('friend',)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('user', 'message', 'room', 'created')
        extra_kwargs = {
            'room': {'write_only': True}
        }
