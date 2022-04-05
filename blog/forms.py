from django.forms import ModelForm, TextInput, PasswordInput
from .models import Post, Comment, Profile, Messages, Dialog
from django import forms
from django.contrib.auth.models import User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('post_name', 'post_text',)
        widgets = {
            'post_text': TextInput(attrs={'class': 'input', 'placeholder': 'Поделиться новостью'}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
        widgets = {
            'comment_text': TextInput(attrs={'class': 'input', 'placeholder': 'Комментировать новость'}),
        }


class UserRegForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)
        widgets = {
            'password': PasswordInput(),
        }


class UserLogForm(forms.Form):
    username = forms.CharField(
        max_length=50)
    password = forms.CharField(max_length=50, widget=PasswordInput())

    class Meta:
        model = User


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class MoreUserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('instagram_link', 'facebook_link',)


class MessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = ('text',)


class GroupForm(ModelForm):
    class Meta:
        model = Dialog
        fields = ('name', 'members',)
