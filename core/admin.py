from django.contrib import admin
from .models import Game, UserState


class GameAdmin(admin.ModelAdmin):
    list_display = ('state', )


class UserStateAdmin(admin.ModelAdmin):
    list_display = ('state', 'user')


admin.site.register(Game, GameAdmin)
admin.site.register(UserState, UserStateAdmin)
