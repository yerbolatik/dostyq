from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json

from userauths.models import User, Profile
from core.models import ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Извлечение имени комнаты из URL-маршрута
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Добавление текущего соединения к группе комнаты
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Удаление текущего соединения из группы комнаты при отключении
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Получение данных сообщения и обработка
        data = json.loads(text_data)
        message = data.get('message')
        sender_username = data.get('sender')

        # Получение отправителя и получателя сообщения
        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.image.url

        except User.DoesNotExist:
            profile_image = ''

        receiver = User.objects.get(username=data['receiver'])

        # Создание и сохранение объекта сообщения в базе данных
        chat_message = ChatMessage(
            sender=sender,
            receiver=receiver,
            message=message
        )
        chat_message.save()

        # Отправка сообщения в группу комнаты для всех участников
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': message,
                'sender': sender_username,
                'profile_image': profile_image,
                'receiver': receiver.username,
            }
        )

    def chat_message(self, event):
        # Отправка сообщения обратно клиенту через WebSocket
        self.send(text_data=json.dumps(event))
