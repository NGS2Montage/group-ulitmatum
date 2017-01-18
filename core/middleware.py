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

        print(request.user)

        # if request.user.is_anonymous():
        #     # How do we get here?
        #     redirect('state-mismatch')

        print(request.user.userstate)
        g = Game.objects.get_current_game()

        if g.state == 'g1' and request.user.userstate.state == 's1' and 'state-mismatch' not in request.path:
            # game already started but user hasn't completed survey 1
            print("not asking for state-mismatch but state mismatched")
            return redirect('state-mismatch')


        print("either correctly asking for state-mismatch or states match")
        # Else: this request is fine, pass it along
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called goes here. Probably we don't have
        # any for this middleware.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("processing view")

        return None
