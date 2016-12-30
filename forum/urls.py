from django.conf.urls import url
# Default Auth for login, logout, login-then-logout
# create Alias of auth_views after it can used
# prevoius in Django 1.8 it was given directly in url as like below
# Eg:-  url(r'^login/$','django.contrib.auth.views.login',name='login')
from django.contrib.auth import views as auth_views

import django.views.defaults

from .import views

from forum.views import HomeView,RecentView, AnnouncementView,GeneralView, UserView

urlpatterns = [

  url(r'^login/$', auth_views.login, name='login'),
  url(r'^logout/$', auth_views.logout, name='logout'),
  url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
  url(r'^password-change/$', auth_views.password_change, name='password_change'),
  url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),
  url(r'^password-reset/$',auth_views.password_reset, name='password_reset'),
  url(r'^password-reset/done/$', auth_views.password_reset_done,
      name='password_reset_done'),
  url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+/$)',
      auth_views.password_reset_confirm, name='password_reset_confirm'),
  url(r'^password-reset/complete/$', auth_views.password_reset_complete,
      name='password_reset_complete'),

  url(r'^404/$',django.views.defaults.page_not_found, name='404'),
  url(r'^register/$', views.user_registration, name='register'),
  url(r'^account/edit/$', views.user_edit, name='edit'),

  url(r'^post/$', views.newquery, name='newquery'),


  # Homepage of the forum
  url(r'^$', HomeView.as_view(),  name='index'),

  # Recent Questions

  url(r'^recent/$', RecentView.as_view(), name='recent'),
  #category wise list
  url(r'^announcement/$', AnnouncementView.as_view(), name='announcement'),
  url(r'^general/$', GeneralView.as_view(), name='general'),
  #list all the questions
  url(r'^question/$', views.all_question, name='question'),

  # add new answer
  url(
    r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
    r'(?P<slug>[-\w]+)/$', views.querydetail , name = 'querydetail'),

  #list user all the questions
  url(r'^myquestions/',views.user_query , name='user_posts'),

  #list all the user answers
  url(r'^myanswers/', views.user_answer, name='user_answers'),

  #edit posted question
  url(r'^(?P<slug>[-\w]+)/$', views.userquestion_edit, name='question_edit'),

  #clsoe the user question
  url(r'^(?P<slug>[-\w]+)/close/$', views.userquery_close, name='question_close'),

  url(r'^(?P<id>\d{2})/(?P<slug>[-\w]+)/comment/$', views.newcomment, name='comment'),

  # url(r'^(?P<slug>[-\w]+)/newanswer/$', views.newanswer , name = 'newanswer'),
  url(r'^(?P<pk>\d+)/(?P<username>[-\w]+)/$', UserView.as_view(), name='userview'),

  url(r'^(?P<id>\d{2})/(?P<slug>[-\w]+)/answeredit/$', views.useranswer_edit, name='editanswer'),
]


