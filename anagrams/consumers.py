import json
import logging
logger = logging.getLogger(__name__)

from annoying.functions import get_object_or_None
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from core.decorators import ws_json_payload, persistent_ws
from core.models import Friend
from .models import UserLetter, LetterTransaction
from .bindings import FriendBinding, LetterTransactionBinding, UserLetterBinding


# Connected to websocket.connect
@channel_session_user_from_http
@persistent_ws
def anagrams_add(message):
    room = "room"
    logger.debug("Adding new websocket to room {}".format(room))
    # Accept connection
    message.reply_channel.send({"accept": True})

    message.channel_session['room'] = room

    logger.error("NEED TO STORE REPLY CHANNELS IN DATABASE SO THAT WE CAN GROUP THEM LATER")

    # Add them to the right group
    Group(message.user.username + "solo").add(message.reply_channel)
    Group("allchat").add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
@ws_json_payload
def anagrams_message(message):
    msg = message['json']
    logger.debug('got a message {}'.format(msg))

    if 'type' in msg and msg['type'] == 'init-game':
        friends_info = [{
            "name": f.friend.username,
            "letters": [ul.letter for ul in UserLetter.objects.filter(user=f.friend)]
        } for f in Friend.objects.filter(user=message.user)]

        response = {
            "type": "init-game",
            "letters": [ul.letter for ul in UserLetter.objects.filter(user=message.user)],
            "username": message.user.username,
            "friends": friends_info
        }
        message.reply_channel.send({
            "text": json.dumps(response)
        })
    elif 'type' in msg and msg['type'] == 'request-letter':
        msg['legal'] = False

        friend = get_object_or_None(Friend, user=message.user, friend__username=msg['from_user'])
        if friend is not None:
            ul = get_object_or_None(UserLetter, user__username=msg['from_user'], letter=msg['letter'])
            if ul is not None:
                LetterTransaction.objects.create(borrower=message.user, letter=ul)
                # Need socket for ul.user here
                Group(msg['from_user'] + "solo").send({
                    "text": json.dumps({
                        "type": "letter-requested",
                        "letter": msg['letter'],
                        "by_user": message.user.username
                    })
                })

                # Tell the requester that this was legal
                msg['legal'] = True

        # Send msg back to sender so they know if it was legal and can update page
        message.reply_channel.send({
            "text": json.dumps(msg)
        })
    elif 'type' in msg and msg['type'] == 'request-approved':
        friend = get_object_or_None(Friend, user=message.user, friend__username=msg['requester'])
        if friend is not None:
            transactions = LetterTransaction.objects.filter(borrower=friend.friend, letter__letter=msg['letter'], letter__user=message.user)
            if transactions.count() != 0:
                transaction = transactions[0]
                transaction.approved = True
                transaction.save()

                Group(msg['requester'] + "solo").send({
                    "text": json.dumps({
                        "type": "request-approved",
                        "letter": msg['letter'],
                        "lender": message.user.username
                    })
                })


# Connected to websocket.disconnect
@channel_session
def anagrams_disconnect(message):
    logger.debug("A websocket named {} just left".format(message.reply_channel))
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)


from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer


class AnagramsServer(JsonWebsocketConsumer):

    http_user = True

    type_mapping = {
        'init-game': 'init_game'
    }

    def connection_groups(self, **kwargs):
        logger.debug("Do you think we have username up here?" + str(kwargs) + str(self.message.user))
        return [self.message.user.username + "solo"]

    def receive(self, content, multiplexer, **kwargs):
        logger.debug("What exactly is in content?" + str(content))

        if 'type' not in content:
            logger.error("No type in content in AnagramsServer " + str(content))

        handler = getattr(self, self.type_mapping[content['type']])
        handler(content, multiplexer)
        # multiplexer.send(content)

    def init_game(self, content, multiplexer):
        friends_info = [{
            "name": f.friend.username,
            "letters": [ul.letter for ul in UserLetter.objects.filter(user=f.friend)]
        } for f in Friend.objects.filter(user=self.message.user)]

        response = {
            "type": "init-game",
            "letters": [ul.letter for ul in UserLetter.objects.filter(user=self.message.user)],
            "username": self.message.user.username,
            "friends": friends_info
        }
        multiplexer.send(response)


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True

    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "anagrams": AnagramsServer,
        "friends": FriendBinding.consumer,
        "lettertransactions": LetterTransactionBinding.consumer,
        "userletters": UserLetterBinding.consumer,
    }

    def connection_groups(self):
        logger.debug("connection_groups " + str(self.message.user))
        return [self.message.user.username + "solo"]
