import logging
logger = logging.getLogger(__name__)

from channels_api.bindings import ResourceBinding

from .models import ChatMessage, Friend
from .serializers import ChatMessageSerializer, FriendSerializer


class FriendBinding(ResourceBinding):

    model = Friend
    stream = "friends"
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(user=self.user)

    @classmethod
    def group_names(self, instance, action):
        logger.debug(str(instance))
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("F has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        return True


class ChatMessageBinding(ResourceBinding):

    model = ChatMessage
    stream = "chats"
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.user)

    @classmethod
    def group_names(self, instance, action):
        logger.debug("chatmessage group_names " + str(instance))
        return ["universal-chat"]

    def create(self, data, **kwargs):
        data['room'] = "universal-chat"
        return super(ChatMessageBinding, self).create(data, **kwargs)

    def has_permission(self, user, action, pk):
        logger.debug("CM has_permission {} {} {}".format(user, action, pk))

        if action in ['update', 'delete']:
            return False

        return True
