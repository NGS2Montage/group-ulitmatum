import logging
logger = logging.getLogger(__name__)

from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer

from core.bindings import ChatMessageBinding, FriendBinding
from .bindings import LetterTransactionBinding, TeamWordBinding, UserLetterBinding


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
        if handler is not None:
            handler(content, multiplexer)


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True

    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "anagrams": AnagramsServer,
        "chats": ChatMessageBinding.consumer,
        "friends": FriendBinding.consumer,
        "lettertransactions": LetterTransactionBinding.consumer,
        "teamwords": TeamWordBinding.consumer,
        "userletters": UserLetterBinding.consumer,
    }

    def connection_groups(self):
        logger.debug("connection_groups " + str(self.message.user))
        return [self.message.user.username + "solo", "universal-chat", "team-1"]
