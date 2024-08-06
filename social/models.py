from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def send_friend_inviation(self,to_profile):
        Invitation.objects.create(from_profile=self,to_profile=to_profile)

    def accept_friend_invitation(self,invitation):
        self.friends.add(invitation.from_profile)
        invitation.from_profile.friends.add(self)
        chat  = apps.get_model('chatting','Chat')
        new_chat = chat.objects.create(
        chat_name = f'{self.user.username}\'s and {invitation.from_profile}\'s chat',
        individual_chat = True)
        new_chat.participants.add(self)
        new_chat.participants.add(invitation.from_profile)  
        new_chat.save()
        invitation.delete()

    def reject_friend_invitation(self,invitation):
        invitation.delete()

    def get_invitations(self):
        return Invitation.objects.filter(to_profile=self)

    def add_friend(self, profile):
        self.friends.add(profile)
        profile.friends.add(self)

    def remove_friend(self, profile):
        self.friends.remove(profile)
        profile.friends.remove(self)

    def get_friends(self):
        return self.friends.all()

    def __str__(self):
        return self.user.username
    
class Invitation(models.Model):
    from_profile = models.ForeignKey(Profile, related_name='sent_invitations', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name='received_invitations', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invitation from {self.from_profile} to {self.to_profile}"

