import user
import operator

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, ListView

from .forms import NewQueryForm, NewAnswerForm, EditQueryForm, CloseQueryForm, UserRegistrationForm, UserEditForm, \
  ProfileEditForm, CommentForm, AnswereditForm, CorrectAnswerForm

from .models import Post, Thread, Profile, Comment, User, Correctanswer

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
      user = user_form.save()
      profile = profile_form.save()
      messages.success(request, 'Profile Updated successfully')
    else:
      messages.error(request, 'Error updating your profile')

  else:
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
  return render(request, 'forum/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form })


@login_required
def newquery(request):
  profile = Profile.objects.all()
  userquestions = Post.objects.filter(user__username=request.user)
  useranswers = Thread.objects.filter(user__username=request.user)
  if request.method == 'POST':
    query_form = NewQueryForm(request.POST)
    if query_form.is_valid():
      new_query = query_form.save(commit=False)
      new_query.user = request.user
      new_query.save()
      messages.success(request, "Added post Succesfully")
      return render(request, 'forum/app/userquerylist.html')
    else:
      messages.error(request, "Post not added ")
  else:
    query_form = NewQueryForm()
  return render(request, "forum/app/newquery.html", {"query_form": query_form,
                                                     "profile": profile,
                                                     "userquestions":userquestions,
                                                     "useranswers":useranswers})


@login_required
def user_query(request):
  post = Post.objects.filter(user__username=request.user)
  return render(request, "forum/app/userquerylist.html", {'post': post})


@login_required
def user_answer(request):
  answers = Thread.objects.filter(user__username=request.user)
  return render(request, 'forum/app/useranswerlist.html', {'answers': answers})


@login_required
def userquery_edit(request, slug):
  edit = get_object_or_404(Post, slug=slug)
  if request.user == edit.user and edit.close == False:
    if request.method == 'POST':
      # instance collect the current question data and update it in save method
      editform = EditQueryForm(instance=edit, data=request.POST)
      if editform.is_valid():
        update = editform.save(commit=False)
        update.user = request.user
        update.save()
        messages.success(request, "Answer update successfully")
      else:
        messages.error(request, "Answer not updated")
    else:
      editform = EditQueryForm(instance=edit)
    return render(request, 'forum/app/userqueryedit.html', {'edit': edit,
                                                            'editform': editform,})
  else:
    return render(request, 404)


def useranswer_edit(request, id, slug):
  query = get_object_or_404(Post, slug=slug)
  answers = query.answer.filter(id=id)
  # foreign key field
  question = Post.objects.get(title=query.title)
  answer = Thread.objects.get(id=id)
  if request.user == answer.user and query.close == False:
    if request.method == 'POST':
      editform = AnswereditForm(instance=answer, data=request.POST)
      if editform.is_valid():
        update = editform.save(commit=False)
        update.user = request.user
        update.post = question
        update.save()
        messages.success(request, "Answer update successfully")
      else:
        messages.error(request, "Answer not updated")
    else:
      editform = AnswereditForm(instance=answer)
    return render(request, 'forum/app/useransweredit.html', {'editform': editform,
                                                             'query': query,
                                                             'answers': answers,
                                                             })


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


def querydetail(request, year, month, day, slug):
  query = get_object_or_404(Post, slug=slug,
                            create__year=year,
                            create__month=month,
                            create__day=day)
  # query details
  answers = query.answer.all()
  comment = Comment.objects.filter(answer__in=answers)

  # query new answer foreign key
  question = Post.objects.get(title=query.title)
  answereach = question.answer.filter()

  correct = query.correctanswer_post.filter()

  if 'post_answer' in request.POST:
    answerform = NewAnswerForm(data=request.POST)
    if answerform.is_valid():
      newanswer = answerform.save(commit=False)
      newanswer.user = request.user
      # verify user anwser exist
      if answereach.filter(user__username=newanswer.user).exists():
        messages.error(request, "answer exist")
      else:
        newanswer.post = question
        newanswer.save()
        messages.success(request, "Newanswer added sucessfully")
    else:
      messages.error(request, "Newanswer not added")

  if 'correct_answer' in request.POST:
    correctanswer = CorrectAnswerForm(data=request.POST)
    if correctanswer.is_valid():
      custom_correctanswer = correctanswer.save(commit=False)
      custom_correctanswer.user = request.user
      custom_correctanswer.post = question
      answer_id = request.POST.get('correctanswer_id', "")
      answer = Thread.objects.get(id=answer_id)
      custom_correctanswer.answer = answer
      if correct.count() < 1:
        custom_correctanswer.save()
        messages.success(request, "correct answer added successfully")
      else:
        messages.error(request, "Correct answer added already. You can't change")
    else:
      messages.error(request, "correct Answer not added")

  if'post_comment' and request.POST:
    commentform = CommentForm(request.POST)
    if commentform.is_valid():
      new_comment = commentform.save(commit=False)
      answer_id = request.POST.get('answer_id', "")
      answer = Thread.objects.get(id=answer_id)
      obj, created = Comment.objects.get_or_create(user=request.user, \
                                                   post=question, \
                                                   answer=answer, comment=new_comment)
      messages.success(request, 'comment added sucessfully')

  answerform = NewAnswerForm()
  correctanswer = CorrectAnswerForm()
  commentform = CommentForm()
  return render(request, 'forum/app/querydetail.html', {'query': query,
                                                        'answers': answers,
                                                        'comment': comment,
                                                        'answerform': answerform,
                                                        'correct': correct,
                                                        'correctanswer': correctanswer,
                                                        'commentform': commentform})

def all_question(request):
  list = Post.objects.filter()

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


class RecentView(ListView):
  model = Post
  queryset = Post.objects.all().order_by('-create')
  context_object_name = 'recent'
  template_name = 'forum/app/recent.html'


class HomeView(ListView):
  model = Post
  paginate_by = '30'
  queryset = Post.objects.all().order_by('-create')
  context_object_name = "recent"
  template_name = 'forum/app/index.html'

  def get_queryset(self):
    result = super(HomeView, self).get_queryset()
    post = Post.objects.all()
    query = self.request.GET.get('query')
    if query:
      query_list = query.split()
      result = post.filter(
        reduce(operator.and_,
               (Q(title__icontains=q) for q in query_list)) |
        reduce(operator.and_,
               (Q(description__icontains=q) for q in query_list))
      )

    return result


  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    context['announcements'] = Post.objects.all().filter(category=Post.ANNOUNCEMENT)
    context['general'] = Post.objects.all().filter(category=Post.GENERAL)
    context['bugreport'] = Post.objects.all().filter(category=Post.BUGREPORT)
    context['tips'] = Post.objects.all().filter(category=Post.TIPSANDTRICKS)
    return context


class AnnouncementView(ListView):
  model = Post
  paginate_by = '10'
  queryset = Post.objects.all().filter(category=Post.ANNOUNCEMENT)
  context_object_name = "announcement"
  template_name = 'forum/app/announcement.html'


class GeneralView(ListView):
  model = Post
  paginate_by = '10'
  context_object_name = "general"
  queryset = Post.objects.all().filter(category=Post.GENERAL)
  template_name = 'forum/app/general.html'


class BugreportView(ListView):
  model = Post
  paginate_by = '10'
  context_object_name = "bugreport"
  queryset = Post.objects.all().filter(category=Post.BUGREPORT)
  template_name = 'forum/app/bugreport.html'


class TipsView(ListView):
  model = Post
  paginate_by = '10'
  context_object_name = "tips"
  queryset = Post.objects.all().filter(category=Post.TIPSANDTRICKS)
  template_name = 'forum/app/tips.html'


class UserView(DetailView):
  model = User
  context_object_name = "user"
  template_name = 'forum/app/userdetail.html'

  def get_context_data(self, **kwargs):
    context = super(UserView, self).get_context_data(**kwargs)
    context['profile'] = Profile.objects.all().get(user=self.request.user)
    context['userquestions'] = Post.objects.filter(user__username=self.request.user)
    context['useranswers'] = Thread.objects.filter(user__username=self.request.user)
    return context
