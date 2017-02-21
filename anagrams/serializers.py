from django.contrib.auth.models import User

from rest_framework import serializers

from .models import LetterTransaction, UserLetter


# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=100)


class UserLetterSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # letter = serializers.CharField(max_length=1)

    class Meta:
        model = UserLetter
        fields = ('pk', 'user', 'letter')


class LetterTransactionSerializer(serializers.ModelSerializer):
    # borrower = UserSerializer()
    # letter = UserLetterSerializer()

    class Meta:
        model = LetterTransaction
        fields = ('pk', 'borrower', 'letter', 'approved')

    # def create(self, validated_data):
    #     borrower_data = validated_data.pop('borrower')
    #     borrower_s = UserSerializer(data=borrower_data)

    #     ul_data = validated_data.pop('letter')
    #     ul_s = UserLetterSerializer(data=ul_data)

    #     if borrower_s.is_valid() and ul_s.is_valid():
    #         borrower = User.objects.get(username=borrower_s.validated_data['username'])
    #         ul = UserLetter.objects.get(user__username=ul_s.validated_data['user']['username'], 
    #                                     letter=ul_s.validated_data['letter'])




            

    # need create and update functions in here since this is all nested up
