from django.shortcuts import redirect

from .models import Game

class GameStateRedirectMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Compare the user's state (request.user.userstate.state) to
        # the current game's state. Redirect to error pages if they are
        # too early or too late.

        g = Game.objects.get_current_game()
        
        if g.state == 'g1' and request.user.userstate.state == 's1':
            # game already started but user hasn't completed survey 1
            return redirect('state-mismatch')

        # Else: this request is fine, pass it along
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called goes here. Probably we don't have
        # any for this middleware.

        return response
