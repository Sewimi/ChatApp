from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
from chatting.models import Chat
from chatting.forms import CreateChatForm
from .models import Profile,Invitation


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('chatting:show_chats')
    return redirect('social:login')


def show_login_page(request):
    if request.user.is_authenticated:
        return redirect('chatting:show_chats')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request,("Login sucessful."))
            return redirect('chatting:show_chats')
        else:
            messages.success(request,("There was an error logging in. Try again"))
            return redirect('social:login')
    else:
        return render(request,'login.html')
    
def show_register_page(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form})  
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if not(form.is_valid()):
            return render(request, 'register.html', {'form': form})       
        user = form.save(commit=False)
        user.save()
        messages.success(request, 'You have singed up successfully.')
        login(request, user)
        return redirect('chatting:show_chats')

    
def logout_page(request):
    logout(request)
    messages.success(request,("You were logged out"))
    return redirect('/')

@login_required
def profile_view(request,username):
    vied_user = get_object_or_404(User,username=username)
    invitations = vied_user.profile.received_invitations.all()

    pending = False
    for invitation in invitations:
        if invitation.from_profile == request.user.profile:
            pending = True


    logged_users_profile = request.user.profile
    user_chats = Chat.objects.filter(participants = logged_users_profile)
    context = {
        'vied_user': vied_user,
        'user_chats' : user_chats,
        'invitations' : invitations,
        'pending_invitation' : pending
    }    
    return render(request, 'profile.html', context)

def search_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            return redirect(reverse('social:profile', kwargs={'username': username}))
    return redirect('chatting:show_chats')

@login_required
def create_chat(request):
    if request.method == 'POST':
        form = CreateChatForm(request.POST,user=request.user)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.chat_name = form.cleaned_data['chat_name']
            test_user = get_object_or_404(Profile,user=get_object_or_404(User,username=request.user.username))
            chat.administrator = test_user
            chat.save()
            form.save_m2m()     
            chat.participants.add(test_user)  

            return redirect('chatting:show_chats')
    else:
        form = CreateChatForm(user=request.user)

    return render(request,'createChat.html',{'form' : form})  

@login_required
def send_invitation(request, username):
    to_profile = get_object_or_404(Profile, user=get_object_or_404(User,username=username))
    request.user.profile.send_friend_inviation(to_profile)
    return redirect('chatting:show_chats')

@login_required
def handle_invitation(request):
    if request.method == "POST":
        action = request.POST.get('action')
        user_profile = request.user.profile
        invitation = get_object_or_404(Invitation, to_profile = user_profile)

        if action == 'accept':
            user_profile.accept_friend_invitation(invitation)

        if action == 'reject':
            user_profile.accept_friend_invitation(invitation)
        return redirect(reverse('social:profile',args=[request.user.username]))
    return redirect('chatting:show_chats')

@login_required
def remove_friend(request, username):
    user = request.user
    try:
        friend_user = User.objects.get(username=username)
        friend_profile = friend_user.profile
        user.profile.remove_friend(friend_profile)
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
    except Profile.DoesNotExist:
        messages.error(request, 'Profile does not exist.')
    return redirect('social:profile', username=username)