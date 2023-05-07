from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from chat.models import ChatRoom


@login_required
def lobby(request, room_id):
    """
    Renders the chat room lobby page with the specified room ID and name.

    Args:
        request (HttpRequest): The HTTP request object.
        room_id (int): The ID of the chat room to render.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    room = get_object_or_404(ChatRoom, id=room_id)
    return render(request, 'chat/lobby.html', {'room_id': room_id, 'room_name': room.room_name})


@login_required
def chat_room_list(request):
    """
    Renders the list of available chat rooms.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/rooms.html', {'chat_rooms': chat_rooms})


@login_required
def create_chat_room(request):
    """
    Renders the page to create a new chat room or creates the room if the request method is POST.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template or a redirect to the new room's lobby.
    """
    if request.method == 'POST':
        room_name = request.POST.get('room_name')

        chat_room, created = ChatRoom.objects.get_or_create(room_name=room_name)
        return render(request, 'chat/lobby.html', {'room_id': chat_room.id,'room_name': chat_room.room_name})
    else:
        return render(request, 'chat/create_room.html')


@login_required
def home(request):
    """
    Renders the chat application's home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    return render(request, 'chat/home.html')
