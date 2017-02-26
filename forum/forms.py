from django import forms  # allow to use default form
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

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

class ImageWidget(forms.FileInput):
    """A ImageField Widget for nonadmin that shows a thumbnail."""

    def __init__(self, attrs={}):   # pylint: disable=E1002,W0102
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):  # pylint: disable=E1002
        output = []
        css = {'style': 'clear:left;float:left;margin:1em 1em 0 0;'}
        output.append(super(ImageWidget, self).render(name, value,
                                                           attrs=css))
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" alt="" '
                           'style="width:100px;height:100px" class="img-responsive"/></a> '
                           % (value.url, value.url)))
        return mark_safe(u''.join(output))

class ProfileEditForm(forms.ModelForm):
  photo = forms.ImageField(label=_('photo'),required=False, error_messages = {'invalid':_("Image files only")}, widget=ImageWidget)
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
