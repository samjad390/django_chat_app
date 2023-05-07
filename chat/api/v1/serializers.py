from rest_framework import serializers
from chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for ChatMessage model.

    This serializer maps ChatMessage model fields to JSON format and includes a 'username' field
    that corresponds to the related User model's username field.

    """

    username = serializers.CharField(source='user.username')

    class Meta:
        model = ChatMessage
        fields = '__all__'
