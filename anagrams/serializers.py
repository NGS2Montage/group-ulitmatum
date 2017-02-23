from rest_framework import serializers

from .models import LetterTransaction, UserLetter


class UserLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLetter
        fields = ('pk', 'user', 'letter')


class LetterTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetterTransaction
        fields = ('pk', 'borrower', 'letter', 'approved')
