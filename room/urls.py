from django.urls import path
from . import views
urlpatterns = [
   path('rooms',views.rooms,name='rooms'),
   path('room/<str:slug>',views.room,name='room'),
]
