from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import UserLetter, LetterTransaction


@admin.register(LetterTransaction)
class LetterTransactionAdmin(VersionAdmin):
    pass


@admin.register(UserLetter)
class UserLetterAdmin(VersionAdmin):
    list_display = ('letter', 'user')
