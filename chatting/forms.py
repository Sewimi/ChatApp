from django import forms
from .models import Chat, ChatGrouping


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


class CreateChatGroupingForm(forms.ModelForm):
    class Meta:
        model = ChatGrouping
        fields = ['group_name']
        widgets = {
            'group_name': forms.TextInput(attrs={'placeholder': 'group_name'}),
        }


class AddChatToGroupingFrom(forms.Form):
    group  = forms.ModelChoiceField(queryset=ChatGrouping.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['group'].queryset = ChatGrouping.objects.filter(belongs_to=user.profile)



    