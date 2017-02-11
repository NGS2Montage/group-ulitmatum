import arrow
import json
import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from annoying.functions import get_object_or_None
from channels import Group

from .models import ChatMessage, Game, WebSocket


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

            if settings.DEBUG:
                from django.contrib import messages
                messages.add_message(request, messages.INFO, "State mismatched while requesting {}".format(request.path))
                messages.add_message(request, messages.INFO, "Required game state {}".format(game_state))
                messages.add_message(request, messages.INFO, "Required user state {}".format(user_state))

            return HttpResponseRedirect(reverse('state-mismatch'))
        return _view
    return _decorator


def persistent_ws(function=None):
    def _decorator(consumer_func):
        def _persist_websocket(message, *args, **kwargs):
            logger.debug("In the decorator, yo")

            ws = get_object_or_None(WebSocket, user=message.user)
            if ws is not None:
                ws.reply_channel = message.reply_channel.name
                ws.save()
            else:
                WebSocket.objects.create(user=message.user, reply_channel=message.reply_channel.name)

            consumer_func(message)
        return _persist_websocket

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def ws_json_payload(function=None):
    def _decorator(consumer_func):
        def _json_converter(message, *args, **kwargs):
            json_payload = None

            try:
                json_payload = json.loads(message['text'])
            except ValueError:
                pass

            if json_payload is not None:
                message['json'] = json_payload

                if 'type' in message['json'] and message['json']['type'] == 'chat':
                    ChatMessage.objects.create(
                        room=message.channel_session['room'],
                        message=message['json']['message'],
                        user=message.user
                    )
                    # Broadcast to listening sockets
                    reply = {
                        "type": "chat",
                        "message": message['json']['message'],
                        "user": message.user.username,
                        "date": arrow.now().format("YYYY-MM-DDTHH:mm:ssZ")
                    }
                    Group("allchat").send({
                        "text": json.dumps(reply)
                    })

                    return  # return here - do not pass on to consumer

            consumer_func(message)
        return _json_converter

    if function is None:
        return _decorator
    else:
        return _decorator(function)
