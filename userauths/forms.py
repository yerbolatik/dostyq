from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.forms import ImageField, FileInput

from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Full Name"}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Mobile No."}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"placeholder": "Email Address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email',
                  'phone', 'gender', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "with-border"


class ProfileUpdateForm(forms.ModelForm):
    image = ImageField(widget=FileInput)

    class Meta:
        model = Profile
        fields = [
            'cover_image',
            'image',
            'full_name',
            'bio',
            'about_me',
            'phone',
            'gender',
            'relationship',
            'friends_visibility',
            'country',
            'city',
            'state',
            'address',
            'working_at',
            'instagram',
            'whatsapp',
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, label='Email', widget=forms.EmailInput(
        attrs={'autocomplete': 'email'}))
