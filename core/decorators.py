from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Game


def game_state_required(user_state, game_state, *dec_args, **dec_kwargs):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_anonymous():
                return view_func(request, *args, **kwargs)

            current_game_state = Game.objects.get_current_game().state
            current_user_state = request.user.userstate.state

            if current_game_state == game_state and current_user_state == user_state:
                return view_func(request, *args, **kwargs)

            if current_game_state in dec_kwargs and current_user_state in dec_kwargs[current_game_state]:
                return HttpResponseRedirect(reverse(dec_kwargs[current_game_state][current_user_state]))

            return HttpResponseRedirect(reverse('state-mismatch'))
        return _view
    return _decorator
