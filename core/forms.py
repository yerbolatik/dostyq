from django import forms
from core.models import Group, GroupChat
from userauths.models import User


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name', 'description', 'images']
