
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from dash.helpers.chat_common import (get_last_10_messages, save_chat,
                                      update_chat_online, update_last_login)
from dash.helpers.file import base64_file, compress_image


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new
        self.chat_type = None  # new

    # async def online(self, data):
    #     # TODO : online
    #     # data = json.loads(data)
    #     # print(data)
    #     # member = await get_chat_member(self, self.room_name, self.user.id)
    #     content = {
    #         'command': 'online',
    #         'online': data['online'],
    #         # 'user_id': self.user.id,
    #         'member_online_id': self.user.id,
    #         # 'member': member,
    #     }
    #     return await self.send_chat_message(content)

    # async def typing(self, data):
    #     # TODO : typing
    #     # data = json.loads(data)
    #     # print(data)
    #     content = {
    #         'data': {
    #             'command': 'typing',
    #             'typing': data['typing'],
    #             # 'user_id': self.user.id,
    #             'member_typing_id': self.user.id,
    #         }
    #     }
    #     return await self.send_chat_message(content)

    async def fetch_messages(self, data):
        # print(data)
        # print("fetch_messages")
        self.chat_type = 'chat' if data['chat_type'] is None else data['chat_type']
        # print(self.chat_type)
        messages = await get_last_10_messages(self, self.room_name, self.user.id, self.chat_type)
        # member = await get_chat_member(self, self.room_name, self.user.id)
        content = {
            'data': {
                'command': 'fetch_messages',
                # 'member': member,
                'messages': self.messages_to_json(messages)
            }
        }
        return await self.send_message(content)

    async def new_message(self, data):
        """
        save chat message to DB
        """
        chat_session_id = self.room_name
        user = self.user
        # print(user)
        # print(user.id)

        # # save message
        image = None
        if data['message_type'] == 'image':
            data_image = base64_file(data['image'])
            image = compress_image(data_image)
            # print(image)

        message = await save_chat(self, user, chat_session_id, data['message'], image, self.chat_type)

        # # add message to array result
        result = []
        result.append(self.message_to_json(message))

        content = {
            'command': 'new_message',
            'messages': result,
        }
        return await self.send_chat_message(content)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.room = self.room_name
        self.user = self.scope["user"]  # new

        # reject connection if not auth user
        if self.user.is_anonymous:
            await self.close()

        # print("user connect: ", self.user)

        # update user last login
        await update_last_login(self, self.user.id)

        # update userprofile is_online = True
        await update_chat_online(self.user, True)

        # broadcast user is online to room
        # await self.online({
        #     'online': True,
        # })

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # update user is_online = False
        await update_chat_online(self.user, False)
        # broadcast user is offline to room
        # TODO : disconnect
        # await self.online({
        #     'online': False,
        # })

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # Send message to room group
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, data):
        # print(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    # Receive message from room group
    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data': message
        }))

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        # print(message)
        return {
            'id': message['id'],
            'user': message['user'],
            'nama': message['nama'],
            'message': message['message'],
            'image': message['image'],
            'is_read': bool(message['is_read']),
            'created': str(message['created'])
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        # 'typing': typing,
        # 'online': online,
    }
