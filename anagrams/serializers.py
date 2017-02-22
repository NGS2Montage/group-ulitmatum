from django.contrib.auth.models import User

from rest_framework import serializers

from core.models import Friend
from .models import LetterTransaction, UserLetter


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


class UserLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLetter
        fields = ('pk', 'user', 'letter')


class LetterTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetterTransaction
        fields = ('pk', 'borrower', 'letter', 'approved')
