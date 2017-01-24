from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to

from .models import Game


@render_to('state-mismatch.html')
@login_required
def state_mismatch(request):
    context = {
        "game": Game.objects.get_current_game()
    }
    # fill in context dict with stuff to pass to template as needed
    return context
