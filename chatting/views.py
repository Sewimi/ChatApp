from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat
from .forms import SendMessageForm, LeaveChatForm, DeleteChatForm

def show_chat_list(request):
    user_profile = request.user.profile
    user_chats = Chat.objects.filter(participants = user_profile)
    context = {
        'user_chats' : user_chats,
    }
    return render(request,'your_chats.html',context)

def show_chat(request, chat_id):
    chat = Chat.objects.get(id = chat_id)
    message_form = SendMessageForm()
    context = {
        "chat" : chat,
        "message_form" : message_form
    }
    
    return render(request, 'chat.html',context)

@login_required
def leave_chat(request):
    if request.method == 'POST':
        form = LeaveChatForm(request.POST)
        if form.is_valid():
            chat_id = form.cleaned_data['chat_id']
            chat = get_object_or_404(Chat, id=chat_id)
            chat.leave_user(request.user.profile)   
    return redirect('home')

@login_required
def delete_chat(request):
    if request.method == 'POST':
        form = DeleteChatForm(request.POST)
        if form.is_valid():
            chat_id = form.cleaned_data['chat_id']
            chat = get_object_or_404(Chat, id=chat_id)
            if chat.administrator == request.user.profile:
                chat.delete_chat()   
    return redirect('home')

@login_required
def send_message(request,chat_id):
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            chat_id = form.cleaned_data['chat_id']
            content  = form.cleaned_data['content']
            sender = request.user.profile
            chat = get_object_or_404(Chat, id=chat_id)
            chat.send_message(sender,content)
        else:
            print(form.errors)
    return redirect(reverse('chatting:chat',args=[chat_id]))  

