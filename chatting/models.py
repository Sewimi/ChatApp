from django.db import models

class ChatGrouping(models.Model):
    belongs_to = models.ForeignKey('social.Profile', related_name='users_groupings', on_delete=models.CASCADE, null=True,default=None, blank=True)
    group_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.group_name



class Chat(models.Model):
    chat_name = models.CharField(max_length=90)
    participants = models.ManyToManyField('social.Profile')
    administrator = models.ForeignKey('social.Profile',on_delete=models.SET_NULL,null=True,related_name='admin_chats')
    individual_chat = models.BooleanField(default=False)
    group = models.ManyToManyField('ChatGrouping', related_name = 'chat_groups', blank=True)

    def send_message(self, sender, content):
        message = Message.objects.create(chat=self, sender=sender, content=content)
        return message

    def delete_message(self, message_id):
        Message.objects.filter(id=message_id, chat=self).delete()

    def remove_chat_member(self, profile_object):
        self.participants.remove(profile_object)

    def delete_chat(self):
        Message.objects.filter(chat=self).delete()
        self.delete()

    def add_to_group(self,grouping_obj):
        try:
            self.group.add(grouping_obj)
            self.save()
        except Exception:
            print("there was an exception")

    def delete_from_groups(self, profile):
        try:
            groups_to_remove = self.group.filter(belongs_to=profile)

            self.group.remove(*groups_to_remove)
        except Exception as e:
            print(f"Error occurred: {e}")

        
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('social.Profile', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField('social.Profile', related_name='read_messages')

    def __str__(self):
        return f"{self.sender}:  {self.content[:50]}"

    class Meta:
        ordering = ['timestamp']

