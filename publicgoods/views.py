from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to

from core.decorators import game_state_required

import re

valid_state_redirects = {
    "w2": {
        "s2": "public-goods-survey",
        "t2": "public-goods-tutorial",
        "w2": "public-goods-waiting",
    }
}


@game_state_required(user_state="g2", game_state="g2", **valid_state_redirects)
@render_to('publicgoods/game.html')
@login_required
def game(request):
    
    def is_valid_number(s):
        f = 0
        try:
            f = float(s)
            if not re.match(r'^[0-9]*\.?[0-9]{2}$', s):
                return "the amount format is invalid"
            else:
                return ""  
        except ValueError:
            return "the dollar amount is not a number"


    context = {}
    context["error"] = ""

    if (request.method == 'POST'):
        
        d_amt = request.POST["dollar_amt"]

        # validate the dollar amount
        error = is_valid_number(d_amt)
        result = 0
        if (len(error) == 0):
            d_amt = float(d_amt)
            result = d_amt
        else:
            result = 0
            context["error"] = error

        context["d_amt"] = result
    else:
        context["d_amt"] = 0

    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="w2", game_state="w2", **valid_state_redirects)
@render_to('publicgoods/waiting.html')
@login_required
def waiting_room(request):
    
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context


@game_state_required(user_state="t2", game_state="w2", **valid_state_redirects)
@render_to('publicgoods/tutorial.html')
@login_required
def tutorial(request):
    return {}


@game_state_required(user_state="s2", game_state="w2", **valid_state_redirects)
@render_to('publicgoods/survey.html')
@login_required
def survey(request):
    return {}
