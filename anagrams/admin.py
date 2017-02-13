from django.contrib import admin
from .models import UserLetter


class UserLetterAdmin(admin.ModelAdmin):
    list_display = ('letter', 'user')

admin.site.register(UserLetter, UserLetterAdmin)
