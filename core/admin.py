from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Game, UserState


@admin.register(Game)
class GameAdmin(VersionAdmin):
    list_display = ('state', )


@admin.register(UserState)
class UserStateAdmin(admin.ModelAdmin):
    list_display = ('state', 'user')
