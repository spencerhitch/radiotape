from django import forms
from django.contrib.auth.forms import UserCreationForm
from rec.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
 
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
 
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class MixForm(forms.Form):
    title = forms.CharField(max_length=25)

class RemixForm(forms.Form):
    title = forms.CharField(max_length=25)
    parent_id = forms.IntegerField()

class TrackForm(forms.Form):
    mix_id = forms.IntegerField()
    sound_id = forms.IntegerField()
    offset = forms.IntegerField()
    volume = forms.IntegerField()
    title = forms.CharField(max_length=25, required=False)

class UploadTrackForm(forms.Form):
    mix_id = forms.IntegerField()
    sound = forms.FileField()
    offset = forms.IntegerField()
    volume = forms.IntegerField()
    title = forms.CharField(max_length=25, required=False)

class MixCommentForm(forms.Form):
    mix_id = forms.IntegerField()
    content = forms.CharField(max_length=500, required=False)

class TrackCommentForm(forms.Form):
    sound_id = forms.IntegerField()
    content = forms.CharField(max_length=500, required=False)

class FavoriteMixForm(forms.Form):
    removing = forms.CharField(max_length=5)

class ProfilePictureForm(forms.Form):
    image = forms.ImageField()

class FollowForm(forms.Form):
    unfollowing = forms.CharField(max_length=5)