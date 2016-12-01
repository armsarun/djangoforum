from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField



class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  date_of_birth = models.DateField(blank=True, null=True)
  photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

  def __str__(self):
    return 'Profile for user {}'.format(self.user.username)

# each query goes under this model
class Post(models.Model):
  # category field objects created
  ANNOUNCEMENT = 'AN';
  BUGREPORT = 'BR';
  TIPSANDTRICKS = 'TT';
  GENERAL = 'GR';

  #assign value to category
  CATEGORY_CHOICES=((ANNOUNCEMENT,
                     'Announcement'),
                    (BUGREPORT,
                     'Bug Report'),
                    (TIPSANDTRICKS,
                     'Tips and tricks'),
                    (GENERAL,
                     'General')
                    )
  user = models.ForeignKey(User)
  title = models.CharField(max_length=255)
  description = RichTextUploadingField(config_name='custom_ckeditor')
  category= models.CharField(max_length=2,choices=CATEGORY_CHOICES,default=GENERAL)
  create = models.DateTimeField(auto_now=True)
  slug = AutoSlugField(populate_from='title',
                       unique_with=['create__month'],
                       )
  close = models.BooleanField(default=False)
  closed_reason = models.TextField(max_length=255, null=True)
  closed_time = models.DateTimeField(auto_now=True)
  def __unicode__(self):
    return self.title

  def __str__(self):
    return self.title

# uset for the simplification of single detail view
  def get_absolute_url(self):
    return reverse('newanswer',
                   args=[self.create.year,
                         self.create.strftime('%m'),
                         self.create.strftime('%d'),
                         self.slug,])

class Thread(models.Model):
  user = models.ForeignKey(User)
  post = models.ForeignKey(Post, related_name='answer')
  content = RichTextUploadingField(config_name='custom_ckeditor')
  create = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.content











