import logging
logger = logging.getLogger(__name__)

from django.db.models import Q

# from channels.binding.websockets import WebsocketBinding
from channels_api.bindings import ResourceBinding

from .models import LetterTransaction, UserLetter
from .serializers import LetterTransactionSerializer, UserLetterSerializer


class UserLetterBinding(ResourceBinding):

    model = UserLetter
    stream = "userletter"
    serializer_class = UserLetterSerializer
    queryset = None
    # fields = ["letter"]

    def get_queryset(self):
        # logger.debug("What's on self? {}".format(self.user))
        return UserLetter.objects.filter(user=self.user)

    @classmethod
    def group_names(self, instance):
        logger.debug(str(instance))
        # return ["userletter-updates"]
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("UL has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        return True


class LetterTransactionBinding(ResourceBinding):

    model = LetterTransaction
    stream = "lettertransaction"
    serializer_class = LetterTransactionSerializer
    # queryset = LetterTransaction.objects.all()
    # fields = ["borrower", "letter__letter", "letter__user__username", "approved"]

    def get_queryset(self):
        # logger.debug("What's on self? {}".format(self.user))
        return LetterTransaction.objects.filter(Q(borrower=self.user) | Q(letter__user=self.user))

    @classmethod
    def group_names(self, instance, action):
        return [instance.borrower.username + "solo", instance.letter.user.username + "solo"]

    def has_permission(self, user, action, pk):
        # instance = LetterTransaction.objects.get(pk=pk)
        logger.debug("TR has_permission {} {} {}".format(user, action, pk))
        return True
