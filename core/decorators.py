import json
import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from channels import Channel

from .models import Game


def game_state_required(user_state, game_state, *dec_args, **dec_kwargs):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_anonymous():
                return view_func(request, *args, **kwargs)

            current_game_state = request.user.userstate.game.state.state_code
            current_user_state = request.user.userstate.state.state_code

            if current_game_state == game_state and current_user_state == user_state:
                return view_func(request, *args, **kwargs)

            if current_game_state in dec_kwargs and current_user_state in dec_kwargs[current_game_state]:
                return HttpResponseRedirect(reverse(dec_kwargs[current_game_state][current_user_state]))

            if settings.DEBUG:
                from django.contrib import messages
                messages.add_message(request, messages.INFO, "State mismatched while requesting {}".format(request.path))
                messages.add_message(request, messages.INFO, "Required game state {}".format(game_state))
                messages.add_message(request, messages.INFO, "Required user state {}".format(user_state))

            return HttpResponseRedirect(reverse('redirect'))
        return _view
    return _decorator


def ws_json_payload(function=None):
    def _decorator(consumer_func):
        def _view(message, *args, **kwargs):
            logger.debug("In the decorator, yo")

            json_payload = None

            try:
                json_payload = json.loads(message['text'])
            except ValueError:
                pass

            if json_payload is not None:
                message['json'] = json_payload

                if 'type' in message['json'] and message['json']['type'] == 'chat':
                    logger.debug("This message was a chat, send it off ({}) {}".format(message.channel_session['room'], message['json']['message']))
                    Channel("chat-messages").send({
                        "room": message.channel_session['room'],
                        "message": message['json']['message'],
                        "username": message.user.username
                    })
                    return  # return here - do not pass on to consumer

            logger.debug("This message was not a chat, send it on")
            consumer_func(message)
        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)

