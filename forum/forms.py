from django import forms #allow to use default form
from django.contrib.auth.models import User
from .models import Profile, Post, Thread

class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ('username', 'first_name', 'email')

  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
      raise forms.ValidationError('Passwords don\'t match.')
    return cd['password2']


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

class NewQueryForm(forms.ModelForm):
   class Meta:
     model = Post
     fields = ('title','description','category')

class NewAnswerForm(forms.ModelForm):
  class Meta:
    model = Thread
    fields = ('content',)

class EditQueryForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title','description','category')

class CloseQueryForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('close','closed_reason')






