from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewQueryForm, NewAnswerForm,EditQueryForm, CloseQueryForm, UserRegistrationForm, UserEditForm, ProfileEditForm

from .models import Post, Thread, Profile

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
    user_form = UserEditForm(instance=request.user,data=request.POST)
    profile_form = ProfileEditForm(instance=request.user.profile,
                               data=request.POST,
                               files=request.FILES)
    if user_form.is_valid()and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Profile Updated successfully')
    else:
      messages.error(request, 'Error updating your profile')

  else:
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
  return  render(request, 'forum/profile_edit.html', {'user_form':user_form, 'profile_form':profile_form})


@login_required
def newquery(request):
  if request.method == 'POST':
    query_form = NewQueryForm(request.POST)
    if query_form.is_valid():
      new_query = query_form.save(commit=False)
      new_query.user = request.user
      new_query.save()
      messages.success(request,"Added post Succesfully")
      return render(request,'forum/app/index.html')
    else:
      messages.error(request,"Post not added ")
  else:
    query_form = NewQueryForm()
  return render(request, "forum/app/newquery.html", {"query_form":query_form})


def newanswer(request, year, month, day, slug):
  query = get_object_or_404(Post,slug = slug,
                            create__year = year,
                            create__month = month,
                            create__day = day)

  answers = query.answer.all()
  #get the foreign key from the Question table
  question = Post.objects.get(title=query.title)
  if request.method == 'POST':
    answer_form = NewAnswerForm(request.POST)
    if answer_form.is_valid():
      new_answer = answer_form.save(commit=False)
      new_answer.user = request.user
      new_answer.post = question
      new_answer.save()
  else:
    answer_form = NewAnswerForm()
  return render(request, 'forum/app/newanswer.html', {'query': query,
                                                       'answers':answers,
                                                       'answer_form':answer_form})


def all_question(request):
  list = Post.objects.all()

  #search all the queries
  search_word = request.GET.get("query")
  if search_word:
    # list = list.annotate(search=SearchVector('title','description')).filter(search=search_word)
    #Stemmer algorithm not used
    list = list.filter(
      Q(title__icontains=search_word)|
      Q(description__icontains=search_word)
    ).distinct()
  return render(request, "forum/app/allquestion.html", {'list':list})


def index(request):
  collect_all = Post.objects.all()
  recent = collect_all.order_by('-create')
  announcement = collect_all.filter(category=Post.ANNOUNCEMENT)
  general = collect_all.filter(category=Post.GENERAL)
  bug_report = collect_all.filter(category=Post.BUGREPORT)
  tips = collect_all.filter(category=Post.TIPSANDTRICKS)
  return render(request,"forum/app/index.html", {'recent': recent,
                                                 'announcement':announcement,
                                                 'general':general,
                                                 'bugreport':bug_report,
                                                 'tips':tips})

@login_required
def user_query(request):
    post = Post.objects.filter(user__username=request.user)
    return render(request, "forum/app/userquerylist.html", {'post':post})


@login_required
def user_answer(request):
  answers = Thread.objects.filter(user__username=request.user)
  return render(request, 'forum/app/useranswerlist.html', {'answers':answers})

@login_required
def userquestion_edit(request, slug):
  edit = get_object_or_404(Post, slug=slug)
  if request.user == edit.user :
    if request.method == 'POST':
      # instance collect the current question data and update it in save method
      editform = EditQueryForm(instance=edit, data = request.POST)
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
  if request.user == edit.user:
    if request.method == 'POST':
      closeform = CloseQueryForm(instance=edit, data=request.POST )
      if closeform.is_valid():
        closeform.save()
        messages.success(request, 'question closed successfully')
      else:
        messages.error(request, 'question unable to close')
    else:
      closeform = CloseQueryForm(instance=edit)
    return render(request, 'forum/app/userqueryclose.html', {'closeform': closeform})
  else:
    return render(request,404)
