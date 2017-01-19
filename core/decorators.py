from django.http import HttpResponseRedirect
from django.urls import reverse


def game_state_required(game_state, user_state, **kwargs):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if (request.user.userstate.state == user_state and
                Game.objects.get_current_game().state == game_state):
                return view_func(request, *args, **kwargs)

            return HttpResponseRedirect(reverse('state-mismatch'))
        return _view
    return _decorator

