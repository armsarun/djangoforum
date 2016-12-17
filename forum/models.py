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
  ANNOUNCEMENT = 'Announcement';
  BUGREPORT = 'Bug Report';
  TIPSANDTRICKS = 'Tips and tricks';
  GENERAL = 'General';

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
  description = RichTextUploadingField(config_name='default')
  category= models.CharField(max_length=255,choices=CATEGORY_CHOICES,default=GENERAL)
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
    return reverse('querydetail',
                   args=[self.create.year,
                         self.create.strftime('%m'),
                         self.create.strftime('%d'),
                         self.slug,])

class Thread(models.Model):
  user = models.ForeignKey(User, related_name='thread_user')
  post = models.ForeignKey(Post, related_name='answer')
  content = RichTextUploadingField(config_name='default')
  create = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.content

  class Meta:
    unique_together = ('user','post','content')













