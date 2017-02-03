import logging
logger = logging.getLogger(__name__)

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from core.decorators import ws_json_payload


# Connected to websocket.connect
@channel_session_user_from_http
def anagrams_add(message):
    room = "room"
    logger.debug("Adding new websocket to room {}".format(room))
    # Accept connection
    message.reply_channel.send({"accept": True})

    message.channel_session['room'] = room

    logger.error("NEED TO STORE REPLY CHANNELS IN DATABASE SO THAT WE CAN GROUP THEM LATER")

    # Add them to the right group
    Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
@ws_json_payload
def anagrams_message(message):
    logger.debug('got a message {}'.format(message.keys()))


# Connected to websocket.disconnect
@channel_session
def anagrams_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
