import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from chat.models import ChatMessage, ChatRoom


class ChatConsumer(WebsocketConsumer):
    """
    WebSocket consumer for handling chat room connections and messages.
    """
    def connect(self):
        """
        Called when a client tries to connect to the chat room.

        Gets the `room_id` from the URL route parameters and adds the consumer
        to the room group for broadcasting messages to all connected clients.

        Accepts the WebSocket connection.
        """
        try:
            self.room_id = int(self.scope["url_route"]["kwargs"]["room_id"])
        except KeyError:
            # fallback for WebSocket requests that don't include `url_route` in scope
            self.room_id = int(self.scope['path'].split('/')[-2])
        self.chat_room = ChatRoom.objects.filter(id=int(self.room_id)).first()
        self.room_group_name = "chat_%s" % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.

        Removes the consumer from the room group.
        """
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Called when the consumer receives a WebSocket message from the client.

        Creates a `ChatMessage` object from the message text and user ID,
        saves it to the database, and sends the message to the room group
        for broadcasting to all connected clients.

        `text_data` should be a JSON string with the following keys:
        - "message": the text of the chat message
        - "user_name": the display name of the message sender
        - "user_id": the ID of the message sender (used to link to the user profile)
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_name = text_data_json["user_name"]
        user_id = text_data_json["user_id"]

        user = User.objects.filter(id=user_id).first()
        chat_message = ChatMessage(chat_room=self.chat_room, message=message, user=user)
        chat_message.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": {'text': message,  'user_name': user_name}}
        )

    def chat_message(self, event):
        """
        Called when the consumer receives a message from the room group.

        Sends the message data to the WebSocket client.
        """
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
