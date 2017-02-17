from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class UserLetterSerializer(serializers.Serializer):
    user = UserSerializer()
    letter = serializers.CharField(max_length=1)


class LetterTransactionSerializer(serializers.Serializer):
    borrower = UserSerializer()
    letter = UserLetterSerializer()
    approved = serializers.BooleanField()
