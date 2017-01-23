import logging
logger = logging.getLogger(__name__)

from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http


# Connected to websocket.connect
@channel_session_user_from_http
def anagrams_add(message):
    room = "room"
    logger.error("Adding new websocket to room {}".format(room))
    # Accept connection
    message.reply_channel.send({"accept": True})

    message.channel_session['room'] = room

    # Add them to the right group
    Group("chat-%s" % room).add(message.reply_channel)

    # Group("chat-%s" % message.user.username[0]).add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def anagrams_message(message):
    logger.error('got a message')
    Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
    })


# Connected to websocket.disconnect
@channel_session
def anagrams_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

