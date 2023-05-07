from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.models import ChatMessage
from chat.api.v1.serializers import ChatMessageSerializer


@api_view(['GET'])
def messages(request, room_id):
    """
    API endpoint to retrieve all chat messages for a given chat room.

    Args:
        request (rest_framework.request.Request): The HTTP request object.
        room_id (int): The ID of the chat room to retrieve messages for.

    Returns:
        rest_framework.response.Response: A response object containing the serialized chat messages.
    """
    chat_messages = ChatMessage.objects.filter(chat_room__id=room_id).order_by('created_at')
    serializer = ChatMessageSerializer(chat_messages, many=True)
    return Response({"message": serializer.data})
