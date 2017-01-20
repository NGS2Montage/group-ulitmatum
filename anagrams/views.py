from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to

from core.decorators import game_state_required


valid_state_redirects = {
    "w1": {
        "s1": "anagrams-survey",
        "t1": "anagrams-tutorial",
        "w1": "anagrams-waiting",
    }
}


@game_state_required(user_state="g1", game_state="g1", **valid_state_redirects)
@render_to('anagrams/game.html')
@login_required
def game(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="w1", game_state="w1", **valid_state_redirects)
@render_to('anagrams/waiting.html')
@login_required
def waiting_room(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="t1", game_state="w1", **valid_state_redirects)
@render_to('anagrams/tutorial.html')
@login_required
def tutorial(request):
    return {}


@game_state_required(user_state="s1", game_state="w1", **valid_state_redirects)
@render_to('anagrams/tutorial.html')
@login_required
def survey(request):
    return {}
