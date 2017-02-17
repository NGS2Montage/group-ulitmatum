import logging
logger = logging.getLogger(__name__)

from django.db import models

from channels.binding.websockets import WebsocketBinding

from .models import UserLetter, LetterTransaction


class UserLetterBinding(WebsocketBinding):

    model = UserLetter
    stream = "userletter"
    fields = ["letter"]

    @classmethod
    def group_names(self, instance):
        logger.debug(str(instance))
        # return ["userletter-updates"]
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        return True


class LetterTransactionBinding(WebsocketBinding):

    model = LetterTransaction
    stream = "lettertransaction"
    fields = ["borrower__username", "letter__letter", "letter__user__username", "approved"]

    @classmethod
    def group_names(self, instance):
        return [instance.borrower.username + "solo", instance.letter.user.username + "solo"]

    def has_permission(self, user, action, pk):
        return True