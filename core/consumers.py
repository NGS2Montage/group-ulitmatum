import logging

logger = logging.getLogger(__name__)


from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http


# from channels import Group

# # Connected to websocket.connect
# def ws_add(message):
#     message.reply_channel.send({"accept": True})
#     Group("chat").add(message.reply_channel)

# # Connected to websocket.receive
# def ws_message(message):
#     Group("chat").send({
#         "text": "[user] %s" % message.content['text'],
#     })

# # Connected to websocket.disconnect
# def ws_disconnect(message):
#     Group("chat").discard(message.reply_channel)


# from channels import Channel, Group
# from channels.sessions import channel_session
# from .models import ChatMessage


# # Connected to chat-messages
# def msg_consumer(message):
#     # Save to model
#     room = message.content['room']
#     ChatMessage.objects.create(
#         room=room,
#         message=message.content['message'],
#     )
#     # Broadcast to listening sockets
#     Group("chat-%s" % room).send({
#         "text": message.content['message'],
#     })


# # Connected to websocket.connect
# @channel_session
# def ws_connect(message):
#     # Work out room name from path (ignore slashes)
#     room = 'my-awesome-chat-room'
#     # Save room in session and add us to the group
#     message.channel_session['room'] = room
#     Group("chat-%s" % room).add(message.reply_channel)


# # Connected to websocket.receive
# @channel_session
# def ws_message(message):
#     # Stick the message onto the processing queue
#     Channel("chat-messages").send({
#         "room": message.channel_session['room'],
#         "message": message['text'],
#     })


# # Connected to websocket.disconnect
# @channel_session
# def ws_disconnect(message):
#     Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)


# # import json
# # import logging

# # from channels import Channel, Group
# # from channels.auth import channel_session_user, channel_session_user_from_http
# # from .models import ChatMessage


# # logger = logging.getLogger(__name__)


# # # Connected to chat-messages
# # def msg_consumer(message):
# #     # Save to model
# #     room = message.content['room']
# #     ChatMessage.objects.create(
# #         room=room,
# #         message=message.content['message'],
# #     )
# #     # Broadcast to listening sockets
# #     Group("chat-%s" % room).send({
# #         "text": message.content['message'],
# #     })


# # # Connected to websocket.connect
# # @channel_session_user_from_http
# # def ws_connect(message):
# #     # Work out room name from path (ignore slashes)
# #     room = "my-awesome-chat-room"
# #     # Save room in session and add us to the group
# #     message.channel_session['room'] = room
# #     Group("chat-%s" % room).add(message.reply_channel)


# # # Connected to websocket.receive
# # @channel_session_user
# # def ws_message(message):
# #     msg = json.loads(message['text'])

# #     if 'type' not in msg:
# #         logger.error('No type in message {}'.format(message))
# #         return

# #     if msg['type'] == 'chat':
# #         # Stick the message onto the processing queue
# #         Channel("chat-messages").send({
# #             "room": message.channel_session['room'],
# #             "message": msg['text'],
# #         })
# #     elif msg['type'] == 'request-letter':
# #         # do all the work for request-letter
# #         # msg probably has keys called from_user and letter
# #         pass
# #     # add other msg type cases here


# # # Connected to websocket.disconnect
# # @channel_session_user
# # def ws_disconnect(message):
# #     Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
