from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chat'),
    path('<str:room_name>/', views.room, name='room'),
    path('add/<id>/', views.create_room, name='create_room'),
    path('ajax/delete-chat/<id>/', views.ajax_delete_chat, name='ajax_delete_chat'),
]
