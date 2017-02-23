import logging
logger = logging.getLogger(__name__)

from django.db.models import Q

# from channels.binding.websockets import WebsocketBinding
from channels_api.bindings import ResourceBinding

from core.models import Friend
from .models import LetterTransaction, UserLetter
from .serializers import FriendSerializer, LetterTransactionSerializer, UserLetterSerializer


class FriendBinding(ResourceBinding):

    model = Friend
    stream = "friends"
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(user=self.user)

    @classmethod
    def group_names(self, instance, action):
        logger.debug(str(instance))
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("F has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        return True


class UserLetterBinding(ResourceBinding):

    model = UserLetter
    stream = "userletters"
    serializer_class = UserLetterSerializer

    def get_queryset(self):
        friends = Friend.objects.filter(user=self.user)

        query = Q(user=self.user)
        for f in friends:
            query = query | Q(user=f.friend)

        return UserLetter.objects.filter(query)

    @classmethod
    def group_names(self, instance, action):
        logger.debug(str(instance))
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("UL has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        return True


class LetterTransactionBinding(ResourceBinding):

    model = LetterTransaction
    stream = "lettertransactions"
    serializer_class = LetterTransactionSerializer

    def get_queryset(self):
        return LetterTransaction.objects.filter(Q(borrower=self.user) | Q(letter__user=self.user))

    @classmethod
    def group_names(self, instance, action):
        return [instance.borrower.username + "solo", instance.letter.user.username + "solo"]

    def has_permission(self, user, action, pk):
        # instance = LetterTransaction.objects.get(pk=pk)
        logger.debug("TR has_permission {} {} {}".format(user, action, pk))
        return True
