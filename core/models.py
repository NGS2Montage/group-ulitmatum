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
    # state = models.CharField(choices=STATE, default=STATE.w1, max_length=20)
    game_code = models.CharField(max_length=20)
    state = models.ForeignKey('GameStates')
    objects = GameManager()

    def __str__(self):
        return u'game={} state={}'.format(self.game_code, self.state)

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
class GameStates(models.Model):
    state_code = models.CharField(max_length=30, unique=True)
    state_name = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)
    allowed_user_states = models.ManyToManyField('GameStates', related_name='allowed_states_admin')
    url_name = models.CharField(max_length=200)

    def __str__(self):
        return self.state_code


@python_2_unicode_compatible
class UserState(TimeStampedModel):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    STATE = Choices('s1', 't1', 'w1', 'g1', 'g2', 's2', 't2', 'w3', 's3', 't3', 'g31', 'g32', 'g33')
    #state = models.CharField(choices=STATE, default=STATE.s1, max_length=20)
    state = models.ForeignKey('GameStates')
    game = models.ForeignKey('Game')

    def __str__(self):
        return u'user={} state={}'.format(self.user.username, self.state)


@python_2_unicode_compatible
class ChatMessage(TimeStampedModel):
    message = models.TextField()
    room = models.CharField(max_length=200)

    def __str__(self):
        return u'{}: {}'.format(self.room, self.message)
