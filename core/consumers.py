import logging
logger = logging.getLogger(__name__)

from channels import Group

from .models import ChatMessage


def chat_consumer(message):
    # Save to model
    logger.debug(message.content)
    room = message.content['room']
    ChatMessage.objects.create(
        room=room,
        message=message.content['message'],
    )
    # Broadcast to listening sockets
    Group("chat-%s" % room).send({
        "text": message.content['message'],
    })
