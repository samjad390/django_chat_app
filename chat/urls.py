from django.urls import path
from chat.views import lobby, home, chat_room_list, create_chat_room

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', chat_room_list, name='rooms'),
    path('create_room/', create_chat_room, name='create_room'),
    path('chat_room/<str:room_id>', lobby, name='chat_room')
]
