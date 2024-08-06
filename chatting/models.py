from django.db import models


class Chat(models.Model):
    chat_name = models.CharField(max_length=90)
    participants = models.ManyToManyField('social.Profile')
    administrator = models.ForeignKey('social.Profile',on_delete=models.SET_NULL,null=True,related_name='admin_chats')

    def send_message(self, sender, content):
        message = Message.objects.create(chat=self, sender=sender, content=content)
        return message

    def delete_message(self, message_id):
        Message.objects.filter(id=message_id, chat=self).delete()

    def leave_user(self, profile_object):
        self.participants.remove(profile_object)

    def delete_chat(self):
        Message.objects.filter(chat=self).delete()
        self.delete()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('social.Profile', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField('social.Profile', related_name='read_messages')

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"

    class Meta:
        ordering = ['timestamp']