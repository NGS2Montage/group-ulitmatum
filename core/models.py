from __future__ import unicode_literals


from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from annoying.fields import AutoOneToOneField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from .managers import GameManager


@python_2_unicode_compatible
class Game(TimeStampedModel):
    STATE = Choices('w1', 'g1', 'w2', 'g2', 'w3', 'g31', 'g32', 'g33')
    state = models.CharField(choices=STATE, default=STATE.w1, max_length=20)
    objects = GameManager()

    def __str__(self):
        return u'state={}'.format(self.state)

    def advance_to_next_state(self):
        if self.state == 'w1':
            # create teams
            # create groups
            # assign anagram letters -> this function should be somewhere in
            #   anagrams dir
            # advance all users at state w1 to g1
            self.state = 'g1'
            self.save()


@python_2_unicode_compatible
class UserState(TimeStampedModel):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    STATE = Choices('s1', 't1', 'w1', 'g1', 'g2', 's2', 't2', 'w3', 's3', 't3', 'g31', 'g32', 'g33')
    state = models.CharField(choices=STATE, default=STATE.s1, max_length=20)

    def __str__(self):
        return u'user={} state={}'.format(self.user.username, self.state)


@python_2_unicode_compatible
class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend')

    def __str__(self):
        return u'user={} friend={}'.format(self.user.username, self.friend.username)


@python_2_unicode_compatible
class ChatMessage(TimeStampedModel):
    message = models.TextField()
    room = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return u'[{}] {} (room: {})'.format(self.user.username, self.message, self.room)


@python_2_unicode_compatible
class WebSocket(models.Model):
    reply_channel = models.CharField(max_length=200)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return u'{} {}'.format(self.user.username, self.reply_channel)
