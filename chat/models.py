from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.chat_room} -> {self.message}"