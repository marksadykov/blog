from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Answer, LikeDislike, Profile, LikeDislikeManager

from taggit.models import Tag

from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from django.utils import timezone

from django.contrib.auth.models import User

from .forms import add_post

############################################
import json
 
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType


from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.csrf import requires_csrf_token


def top_questions():
    questions = Question.objects.all()
    firstSize = 0
    firstId = 0

    secondSize = 0
    secondId = 0

    thirdSize = 0
    thirdId = 0

    for question in questions:
        size = question.votes.likes().count() - question.votes.dislikes().count()
        
        if (size > firstSize):
            thirdSize = secondSize 
            thirdId = secondId

            secondSize = firstSize 
            secondId = firstId

            firstSize = size 
            firstId = question.id

        elif (size > secondSize):

            thirdSize = secondSize 
            thirdId = secondId

            secondSize = size 
            secondId = question.id

        elif (size > thirdSize):

            thirdSize = size 
            thirdId = question.id

    max_list = [firstId, secondId, thirdId]

    return max_list


def post_list(request, tag_slug=None):
	questions = Question.objects.order_by('-pub_date')
	tag = ""
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		questions = questions.filter(tags__in=[tag])

	posts = paginate(questions, request, 3)
	answers = {}
	for question in Question.objects.all():
		answers[question.id] = Answer.objects.filter(question=question.id).count() 

	users = User.objects.all()
	profiles = Profile.objects.all()
	
	top_list = top_questions()
	top_question_0 = Question.objects.get(id = top_list[0])
	top_question_1 = Question.objects.get(id = top_list[1])	
	top_question_2 = Question.objects.get(id = top_list[2])
	
	return render(request, 'index.html', {'posts': posts,'tag':tag,'answers': answers, 'profiles': profiles, 'users': users, 'top_question_0':top_question_0,'top_question_1':top_question_1, 'top_question_2':top_question_2})

def paginate(objects_list, request, obj_per_list = 5):
    paginator = Paginator(objects_list, obj_per_list)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return items


def detail(request, question_id):
	try:
		a = Question.objects.get(id = question_id)
	except:
		raise Http404("Статья не найдена!")

	answers_list = a.answer_set.order_by('-id')
	answers_list_count = a.answer_set.order_by('-id').count()
	users = User.objects.all()
	profiles = Profile.objects.all()
	top_list = top_questions()
	top_question_0 = Question.objects.get(id = top_list[0])
	top_question_1 = Question.objects.get(id = top_list[1])
	top_question_2 = Question.objects.get(id = top_list[2])

	user_id = User.objects.get(username = a.author_id)
	
	return render(request, 'detail.html', {'question': a, 'answers_list': answers_list, 'answers_list_count': answers_list_count, 'profiles': profiles, 'users': users, 'top_question_0':top_question_0,'top_question_1':top_question_1, 'top_question_2':top_question_2, 'user_id':user_id})



def leave_comment(request, question_id):
	try:
		a = Question.objects.get(id = question_id)
	except:
		raise Http404("Статья не найдена!")


	if request.user.is_authenticated:
		a.answer_set.create(author_id  = request.user, answer_text = request.POST['text'])
	else:
		HttpResponseRedirect(reverse('blog:detail', args = (a.id,)))

	return HttpResponseRedirect(reverse('blog:detail', args = (a.id,)))


def newpost_page(request):
	form = add_post()

	top_list = top_questions()
	top_question_0 = Question.objects.get(id = top_list[0])
	top_question_1 = Question.objects.get(id = top_list[1])	
	top_question_2 = Question.objects.get(id = top_list[2])

	return render(request,'newpost.html', {'form': form, 'top_question_0':top_question_0,'top_question_1':top_question_1, 'top_question_2':top_question_2})


def post_new(request):
    if request.method == "POST":
        form = add_post(request.POST)
        if form.is_valid():
        	post = form.save(commit=False)
        	post.author_id = request.user
        	post.pub_date = timezone.now()
        	post.save()
        	form.save_m2m()
        	return HttpResponseRedirect(reverse('blog:newpost_page'))
    else:
    	form = add_post()

    return render(request, 'newpost.html', {'form': form})



def createacc_su(request):
	try:
		user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
		user.save()
		profile = Profile.objects.create(user = user)
		profile.save()
		mes = "Аккаунт создан!"
	except:
		mes = "Вы уже зарегистрированы"
	
	return render(request,'create_acc.html', {'mes': mes})

def createacc(request):
	return render(request,'create_acc.html')


def change_login(request):
	user = User.objects.get(username = request.user)
	if( request.POST.get("username")!=''):
		user.username = request.POST.get("username")
		user.save()

	if( request.POST.get("email")!=''):
		user.email = request.POST.get("email")
		user.save()
		

	if( request.POST.get("firstname")!=''):
		user.first_name = request.POST.get("firstname")
		user.save()	
	
	uname = user.username
	uemail = user.email
	ufirstname = user.first_name

	mes = 'Данные обновлены!'
	return render(request,'change.html', {'mes': mes,'uname': uname, 'uemail': uemail, 'ufirstname': ufirstname})

def change(request):
	user = User.objects.get(username = request.user)
	uname = user.username
	uemail = user.email
	ufirstname = user.first_name
	return render(request,'change.html', {'uname': uname, 'uemail': uemail, 'ufirstname': ufirstname})


class VotesView(View):
    model = None    # Модель данных - Статьи или Комментарии
    vote_type = None # Тип комментария Like/Dislike
 
    def post(self, request, question_id):
        obj = self.model.objects.get(id = question_id)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True
 
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )

def make_top(request, question_id):
	question = Question.objects.get(id = question_id)
	question.id_top_answer = request.POST['obj']
	question.save()

	return HttpResponse(
            json.dumps({
                "top": ": это новый лучший ответ"
            }),
            content_type="application/json"
        )


