from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Game, UserState, ChatMessage, WebSocket, Friend


@admin.register(Game)
class GameAdmin(VersionAdmin):
    list_display = ('state', )


@admin.register(UserState)
class UserStateAdmin(VersionAdmin):
    list_display = ('state', 'user')


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(WebSocket)
class WebSocketAdmin(admin.ModelAdmin):
    pass
