from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from annoying.fields import AutoOneToOneField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from .managers import GameManager


@python_2_unicode_compatible
class Game(TimeStampedModel):
    STATE = Choices('w1', 'g1', 'w2', 'g2', 'w3', 'g3')
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
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    STATE = Choices('s1', 't1', 'w1', 'g1')  # needs more
    state = models.CharField(choices=STATE, default=STATE.s1, max_length=20)

    def __str__(self):
        return u'state={}'.format(self.state)
