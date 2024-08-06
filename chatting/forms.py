from django import forms
from .models import Chat


class CreateChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['chat_name','participants']
        widgets = {
            'chat_name': forms.TextInput(attrs={'placeholder': 'Chat Name'}),
            'participants': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') 
        super(CreateChatForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = user.profile.friends


class DeleteChatForm(forms.Form):
    chat_id = forms.IntegerField(widget=forms.HiddenInput())

class LeaveChatForm(forms.Form):
    chat_id = forms.IntegerField(widget=forms.HiddenInput())

class SendMessageForm(forms.Form):
    chat_id = forms.IntegerField(widget=forms.HiddenInput())
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))