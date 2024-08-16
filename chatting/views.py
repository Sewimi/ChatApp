from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat, ChatGrouping
from .forms import SendMessageForm, LeaveChatForm, DeleteChatForm, CreateChatGroupingForm  , AddChatToGroupingFrom 



def show_chat_list(request):
    user_profile = request.user.profile
    user_chats = Chat.objects.filter(participants = user_profile)
    create_group_form = CreateChatGroupingForm()
    add_to_folder_form = AddChatToGroupingFrom(user = request.user)
    folders = user_profile.users_groupings.all()
    context = {
        'add_to_folder_form' : add_to_folder_form,
        'create_group_form' : create_group_form,
        'user_chats' : user_chats,
        'folders' : folders,
    }
    return render(request,'your_chats.html',context)

def create_group(request):
    if request.method == 'POST':
        form = CreateChatGroupingForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.belongs_to = request.user.profile
            group.save()
            return redirect('chatting:show_chats')
    
    return redirect('chatting:show_chats')

def show_chat(request, chat_id):
    chat = Chat.objects.get(id = chat_id)
    message_form = SendMessageForm()
    messages = chat.messages.all()
    for message in messages:
        message.read_by.add(request.user.profile)
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
    return redirect('chatting:show_chats')

@login_required
def delete_chat(request):
    if request.method == 'POST':
        form = DeleteChatForm(request.POST)
        if form.is_valid():
            chat_id = form.cleaned_data['chat_id']
            chat = get_object_or_404(Chat, id=chat_id)
            if chat.administrator == request.user.profile:
                chat.delete_chat()   
    return redirect('chatting:show_chats')

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

@login_required
def add_chat_to_grouping(request):
    if request.method == 'POST':
        form = AddChatToGroupingFrom(request.POST , user=request.user)
        if form.is_valid():
            chat_id = request.POST.get('chat_id')
            group  = form.cleaned_data['group']
            chat = get_object_or_404(Chat,id = chat_id)
            chat.add_to_group(group)
        else:
            print(form.errors)
    return redirect('chatting:show_chats')  

@login_required
def delete_chat_from_grouping(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        chat = get_object_or_404(Chat,id = chat_id)
        chat.delete_from_groups(profile = request.user.profile)
    
    return redirect('chatting:show_chats')  


@login_required
def delete_member_from_chat(request):
    chat_id = request.GET.get('chat_id')
    chat = get_object_or_404(Chat,id = chat_id)
    if not(chat):
        return redirect('chatting:show_chats')  

    if request.method == 'POST':
        user_to_remove = request.POST.get()
        chat.remove_chat_member(profile_object = user_to_remove )
    else:
        chat_members = chat.participants.all()
        chat_members = chat_members.exclude(user = request.user)
        context = {'chat_members' : chat_members}
        return render(request,'delete_member.html',context)
