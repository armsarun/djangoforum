from PIL import Image
from django import forms  # allow to use default form
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Profile, Post, Thread, Comment, Correctanswer


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
  email = forms.EmailField(
    widget=forms.EmailInput(attrs={'required': 'required'}),
    error_messages={'invalid': 'your custom error message'}
  )

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('date_of_birth', 'photo')

  def clean_photo(self):
    image = self.cleaned_data.get('photo', False)

    if image:

      # validate file size
      if len(image) > (1 * 1024 * 1024):
        raise forms.ValidationError(_('Image file too large ( maximum 1mb )'))
    else:
      raise forms.ValidationError(_("Couldn't read uploaded image"))
    return image


class NewQueryForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'description', 'category')


class NewAnswerForm(forms.ModelForm):
  class Meta:
    model = Thread
    fields = ('content',)


class EditQueryForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'description', 'category')


class CloseQueryForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('close', 'closed_reason')


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('comment',)


class AnswereditForm(forms.ModelForm):
  class Meta:
    model = Thread
    fields = ('content',)


class CorrectAnswerForm(forms.ModelForm):
  class Meta:
    model = Correctanswer
    fields = ('correct_answer',)
