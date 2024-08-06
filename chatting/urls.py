from django.urls import path
from . import views

app_name= 'chatting'

urlpatterns = [
    path('your_chats/',views.show_chat_list,name='show_chats'),
    path('chat/<str:chat_id>/',views.show_chat, name='chat'),
    path('leave_chat/',views.leave_chat,name='leave_chat'),
    path('delete_chat/',views.delete_chat,name='delete_chat'),
    path('send_message/<str:chat_id>/',views.send_message,name='send_message'),
]