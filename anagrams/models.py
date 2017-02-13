from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class UserLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    letter = models.CharField(max_length=1)

    def __str__(self):
        return u'({}) {}'.format(self.user.username, self.letter.upper())
