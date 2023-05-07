from django.urls import path
from chat.api.v1.views import messages

urlpatterns = [
    path('messages/<int:room_id>', messages, name='messages')
]
