import asyncio

from django.db import transaction
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatConsumer
from chat.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User
import json
from asgiref.sync import sync_to_async


def format_message(message):
    return {
        "id": message.id,
        "message": message.message,
        "created_at": message.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "chat_room": message.chat_room.id,
        "user": message.user.id,
        "username": message.user.username
    }


class MessageApiTests(APITestCase):
    def setUp(self):
        user1 = User(username='user1', password='test')
        user1.save()
        user2 = User(username='user2', password='test')
        user2.save()
        chat_room = ChatRoom.objects.create(room_name='test_room')
        chat_room.save()
        ChatMessage.objects.create(user=user1, message='test_message', chat_room=chat_room).save()
        ChatMessage.objects.create(user=user2, message='test_message', chat_room=chat_room).save()

    def test_message_api_when_nothing_exist(self):
        url = '/chat/api/v1/messages/0'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        assert len(resp_data['message']) == 0

    def test_message_api(self):
        chat_room = ChatRoom.objects.get(room_name='test_room')
        url = f'/chat/api/v1/messages/{chat_room.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        chat_messages = ChatMessage.objects.filter(chat_room__id=chat_room.id)
        assert len(resp_data['message']) == len(chat_messages)
        expected_data = []
        for msg in chat_messages:
            expected_data.append(format_message(msg))

        assert resp_data['message'] == expected_data


class ChatConsumerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.chat_room = ChatRoom.objects.create(room_name='test room')

    def tearDown(self):
        self.user.delete()
        self.chat_room.delete()

    def test_chat_consumer(self):
        @transaction.atomic
        async def test_chat():
            communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f'/ws/chat/{self.chat_room.id}/')
            connected, _ = await communicator.connect(timeout=10)
            self.assertTrue(connected)

            message = 'Test message'
            user_name = 'testuser'
            user_id = self.user.id
            data = {
                'message': message,
                'user_name': user_name,
                'user_id': user_id,
            }
            await communicator.send_json_to(data)

            response = await communicator.receive_json_from()
            self.assertEqual(response['message']['text'], message)
            self.assertEqual(response['message']['user_name'], user_name)

            chat_message = await sync_to_async(ChatMessage.objects.filter)(chat_room=self.chat_room, message=message,
                                                                           user=self.user)
            self.assertIsNotNone(chat_message)

            await communicator.disconnect()

        # Call async function from sync context
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(test_chat())
