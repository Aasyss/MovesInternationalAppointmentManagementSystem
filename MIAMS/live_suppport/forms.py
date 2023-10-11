from django import forms
from django.utils.translation import gettext_lazy as _
from live_suppport.models import Chat, ChatMessage


class ChatForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea, label=_('Question'))
    class Meta:
        model = Chat
        fields = ('name','details',)

class ChatMessageForm(forms.ModelForm):
    message = forms.CharField()
    class Meta:
        model = ChatMessage
        fields = ('message',)
