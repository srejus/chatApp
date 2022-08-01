from django.urls import path
from . import views
urlpatterns = [
   path('rooms',views.rooms,name='rooms'),
   path('room/<str:slug>',views.room,name='room'),
   path('chat-settings/<str:slug>',views.chat_setting,name='chat_settings'),
   path('clear-chat/<str:slug>',views.clear_chat,name='clear_chat'),
   path('delete-group/<str:slug>',views.delete_group,name='delete_group'),
   path('create-group',views.create_group,name='create_group'),
   path('search',views.search,name='search'),
]
