import json
import logging
logger = logging.getLogger(__name__)

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from core.decorators import ws_json_payload
from .models import UserLetter


# Connected to websocket.connect
@channel_session_user_from_http
def anagrams_add(message):
    room = "room"
    logger.debug("Adding new websocket to room {}".format(room))
    # Accept connection
    message.reply_channel.send({"accept": True})
    logger.debug("Here is a new websocket named {}".format(message.reply_channel))

    message.channel_session['room'] = room

    logger.error("NEED TO STORE REPLY CHANNELS IN DATABASE SO THAT WE CAN GROUP THEM LATER")

    # Add them to the right group
    Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
@ws_json_payload
def anagrams_message(message):
    msg = message['json']
    logger.debug('got a message {}'.format(msg))

    if 'type' in msg and msg['type'] == 'init-game':
        response = {
            "type": "init-game",
            "letters": [ul.letter for ul in UserLetter.objects.filter(user=message.user)],
            "username": message.user.username,
            "friends": [{
                "name": "USER0",
                "letters": ["X", "E", "H"],
            }, {
                "name": "USER1",
                "letters": ["C", "V", "E"],
            }]
        }
        message.reply_channel.send({
            "text": json.dumps(response)
        })
    elif 'type' in msg and msg['type'] == 'request-letter':
        logger.debug("Letter request not yet implemented")


# Connected to websocket.disconnect
@channel_session
def anagrams_disconnect(message):
    logger.debug("A websocket named {} just left".format(message.reply_channel))
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
