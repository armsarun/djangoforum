import user

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from .forms import NewQueryForm, NewAnswerForm, EditQueryForm, CloseQueryForm, UserRegistrationForm, UserEditForm, \
  ProfileEditForm,CommentForm

from .models import Post, Thread, Profile, Comment


def user_registration(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
      new_user = user_form.save(commit=False)
      new_user.set_password(user_form.cleaned_data['password'])
      new_user.save()
      profile = Profile.objects.create(user=new_user)
      return render(request, 'forum/register_done.html', {'new_user': new_user})
  else:
    user_form = UserRegistrationForm()
  return render(request, 'forum/signup.html', {'user_form': user_form})


@login_required
def user_edit(request):
  if request.method == 'POST':
    user_form = UserEditForm(instance=request.user, data=request.POST)
    profile_form = ProfileEditForm(instance=request.user.profile,
                                   data=request.POST,
                                   files=request.FILES)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Profile Updated successfully')
    else:
      messages.error(request, 'Error updating your profile')

  else:
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
  return render(request, 'forum/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def newquery(request):
  if request.method == 'POST':
    query_form = NewQueryForm(request.POST)
    if query_form.is_valid():
      new_query = query_form.save(commit=False)
      new_query.user = request.user
      new_query.save()
      messages.success(request, "Added post Succesfully")
      return render(request, 'forum/app/allquestion.html')
    else:
      messages.error(request, "Post not added ")
  else:
    query_form = NewQueryForm()
  return render(request, "forum/app/newquery.html", {"query_form": query_form})


def querydetail(request, year, month, day, slug):
  query = get_object_or_404(Post, slug=slug,
                            create__year=year,
                            create__month=month,
                            create__day=day)

  answers = query.answer.all()
  return render(request, 'forum/app/querydetail.html', {'query': query,
                                                        'answers': answers})


@login_required
def newanswer(request, slug):
  query = get_object_or_404(Post, slug=slug)
  question = Post.objects.get(title=query.title)
  answer = question.answer.filter()

  if request.method == 'POST':
    answer_form = NewAnswerForm(request.POST)
    if answer_form.is_valid():
      newanswer = answer_form.save(commit=False)
      newanswer.user = request.user
      #verify user anwser exist
      if answer.filter(user__username=newanswer.user).exists():
        messages.error(request, "answer exist")
      else:
        newanswer.post = question
        newanswer.save()
        messages.success(request, "Newanswer added sucessfully")
    else:
      messages.error(request, "Newanswer not added")
  else:
    answer_form = NewAnswerForm()
  return render(request, 'forum/app/newanswer.html', {'query': query,
                                                      'answer_form': answer_form})


def all_question(request):
  list = Post.objects.all()

  # search all the queries
  search_word = request.GET.get("query")
  if search_word:
    # list = list.annotate(search=SearchVector('title','description')).filter(search=search_word)
    # Stemmer algorithm not used
    list = list.filter(
      Q(title__icontains=search_word) |
      Q(description__icontains=search_word)
    ).distinct()
  return render(request, "forum/app/allquestion.html", {'list': list})


def index(request):
  collect_post = Post.objects.all()
  recent = collect_post.order_by('-create')
  return render(request, "forum/app/index.html", {'recent': recent,})


@login_required
def user_query(request):
  post = Post.objects.filter(user__username=request.user)
  return render(request, "forum/app/userquerylist.html", {'post': post})


@login_required
def user_answer(request):
  answers = Thread.objects.filter(user__username=request.user)
  return render(request, 'forum/app/useranswerlist.html', {'answers': answers})


@login_required
def userquestion_edit(request, slug):
  edit = get_object_or_404(Post, slug=slug)
  if request.user == edit.user and edit.close == False:
    if request.method == 'POST':
      # instance collect the current question data and update it in save method
      editform = EditQueryForm(instance=edit, data=request.POST)
      if editform.is_valid():
        update = editform.save(commit=False)
        update.user = request.user
        update.save()
        messages.success(request, 'Question Updated successfully')
      else:
        messages.error(request, 'Question update failed')
    else:
      editform = EditQueryForm(instance=edit)
    return render(request, 'forum/app/userqueryedit.html', {'edit': edit,
                                                            'editform': editform,})
  else:
    return render(request, 404)


def userquery_close(request, slug):
  edit = get_object_or_404(Post, slug=slug)
  if request.user == edit.user and edit.close == False:
    if request.method == 'POST':
      closeform = CloseQueryForm(instance=edit, data=request.POST)
      if closeform.is_valid():
        closeform.save()
        messages.success(request, 'question closed successfully')
      else:
        messages.error(request, 'question unable to close')
    else:
      closeform = CloseQueryForm(instance=edit)
    return render(request, 'forum/app/userqueryclose.html', {'closeform': closeform})
  else:
    return render(request, 404)

@login_required
def newcomment(request,slug, id):
  query = get_object_or_404(Post, slug=slug)
  #get the exact answer id in all answers
  answers = query.answer.filter(id=id)
  # Foreign key field instances
  question = Post.objects.get(title=query.title)
  answer = Thread.objects.get(id=id)

  comments = answer.comment_answers.filter()
  if request.method == 'POST':
    commentform = CommentForm(request.POST)
    if commentform.is_valid():
      new_comment = commentform.save(commit=False)
      # new_comment.user = request.user
      # new_comment.post = question
      # new_comment.answer = answer
      # new_comment.save()
      obj, created = Comment.objects.get_or_create(user=request.user, \
                                                   post=question,\
                                                   answer=answer,comment=new_comment)
      messages.success(request, "comment added sucessfully")
    else:
      messages.error(request, "comment not added")
  else:
    commentform = CommentForm()
  return render(request,'forum/app/newcomment.html', {'commentform':commentform,
                                                      'query':query,
                                                      'answers': answers,
                                                      'comments':comments})

