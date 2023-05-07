from django.contrib import admin


class ChatRoomModalAdmin(admin.ModelAdmin):

    list_display = ['room_name']
    search_fields = ['room_name']


class MessagesModalAdmin(admin.ModelAdmin):

    list_display = ['chat_room', 'message', 'user', 'created_at']
