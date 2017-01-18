from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from annoying.decorators import render_to

@render_to('anagrams.html')
@login_required
def game(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@render_to('anagrams_waiting.html')
@login_required
def waiting_room(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context
