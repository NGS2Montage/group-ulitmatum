from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from annoying.fields import AutoOneToOneField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from .managers import GameManager


class Game(TimeStampedModel):
    STATE = Choices('w1', 'g1', 'w2', 'g2', 'w3', 'g3')
    state = models.CharField(choices=STATE, default=STATE.w1, max_length=20)
    objects = GameManager()


class UserState(TimeStampedModel):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    STATE = Choices('s1', 't1', 'w1', 'g1')  # needs more
    state = models.CharField(choices=STATE, default=STATE.s1, max_length=20)
