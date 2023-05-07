
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('accounts/', include('user.urls')),
    path('chat/api/v1/', include('chat.api.v1.urls'))
]