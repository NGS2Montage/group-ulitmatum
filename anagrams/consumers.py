import logging
logger = logging.getLogger(__name__)

from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer

from core.bindings import ChatMessageBinding, GroupBinding, UserBinding
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
        "groups": GroupBinding.consumer,
        "lettertransactions": LetterTransactionBinding.consumer,
        "teamwords": TeamWordBinding.consumer,
        "userletters": UserLetterBinding.consumer,
        "users": UserBinding.consumer,
    }

    def connection_groups(self):
        
        team_group = str(self.message.user.group.team)
        groups = [self.message.user.username + "solo", "universal-chat", team_group]
        chat_groups = [str(g) for g in self.message.user.profile.groups.all()]
        groups.extend(chat_groups)

        logger.debug("connection_groups for {}: {}".format(self.message.user, groups))
        
        return groups
