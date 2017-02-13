from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Game, UserState, ChatMessage


@admin.register(Game)
class GameAdmin(VersionAdmin):
    list_display = ('state', )


@admin.register(UserState)
class UserStateAdmin(admin.ModelAdmin):
    list_display = ('state', 'user')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass
