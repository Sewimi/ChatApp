from django.urls import path
from . import views

app_name= 'chatting'

urlpatterns = [
    path('your_chats/',views.show_chat_list,name='show_chats'),
    path('chat/<str:chat_id>/',views.show_chat, name='chat'),
    path('leave_chat/',views.leave_chat,name='leave_chat'),
    path('delete_chat/',views.delete_chat,name='delete_chat'),
    path('send_message/<str:chat_id>/',views.send_message,name='send_message'),
    path('create_group',views.create_group,name='create_group'),
    path('add_chat_to_grouping',views.add_chat_to_grouping,name='add_grouping'),
    path('leave_grouping/',views.delete_chat_from_grouping,name='leave_grouping'),
    path('delete_chat_member/',views.delete_member_from_chat ,name='delete_member'),
]