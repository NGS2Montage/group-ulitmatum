from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from annoying.decorators import render_to

from core.decorators import game_state_required

@game_state_required(game_state="g1", user_state="g1")
@render_to('anagrams.html')
@login_required
def game(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(game_state="w1", user_state="w1", s1="/phase1/survey1/", t1="/phase1/tutorial1/")
@render_to('anagrams_waiting.html')
@login_required
def waiting_room(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context
