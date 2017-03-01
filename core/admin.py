from django.contrib import admin

from reversion.admin import VersionAdmin

from . import models


@admin.register(models.Game)
class GameAdmin(VersionAdmin):
    list_display = ('pk', 'state', 'created')


@admin.register(models.Profile)
class ProfileAdmin(VersionAdmin):
    list_display = ('user', 'state', 'get_groups')

    def get_groups(self, obj):
        return ", ".join([str(g) for g in obj.groups.all()])


@admin.register(models.Group)
class GroupAdmin(VersionAdmin):
    list_display = ('group_name', 'team')

    def group_name(self, obj):
        return str(obj)

@admin.register(models.Team)
class TeamAdmin(VersionAdmin):
    pass


@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WebSocket)
class WebSocketAdmin(admin.ModelAdmin):
    pass
