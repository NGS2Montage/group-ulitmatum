from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to

from core.decorators import game_state_required


valid_state_redirects = {
    "w3": {
        "s3": "group-ultimatums-survey",
        "t3": "group-ultimatums-tutorial",
        "w3": "group-ultimatums-waiting",
    }
}


@game_state_required(user_state="g31", game_state="g31", **valid_state_redirects)
@render_to('groupultimatums/initial.html')
@login_required
def game_initial(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="g32", game_state="g32", **valid_state_redirects)
@render_to('groupultimatums/voting.html')
@login_required
def game_voting(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="g33", game_state="g33", **valid_state_redirects)
@render_to('groupultimatums/final.html')
@login_required
def game_final(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="w3", game_state="w3", **valid_state_redirects)
@render_to('groupultimatums/waiting.html')
@login_required
def waiting_room(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="t3", game_state="w3", **valid_state_redirects)
@render_to('groupultimatums/tutorial.html')
@login_required
def tutorial(request):
    return {}


@game_state_required(user_state="s3", game_state="w3", **valid_state_redirects)
@render_to('groupultimatums/survey.html')
@login_required
def survey(request):
    return {}
