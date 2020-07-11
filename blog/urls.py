from django.urls import path
from . import views

from django.conf.urls import url

from .models import Question, Answer, LikeDislike, Profile, LikeDislikeManager

from django.contrib.auth.decorators import login_required


app_name = 'blog'
urlpatterns = [
	path('', views.post_list, name = 'post_list'),
	path('popularpost', views.post_list, name = 'popularpost'),
	path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),

	path('<int:question_id>/', views.detail, name = 'detail'),
	path('<int:question_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),

	path('newpost/', views.newpost_page, name = 'newpost_page'),
	path('newpost/add', views.post_new, name='post_new'),

	path('createacc', views.createacc, name='createacc'),
	path('createacc/su', views.createacc_su, name='createaccsu'),

	path('change', views.change, name='change'),
	path('change/login', views.change_login, name='changelogin'),

    path('<int:question_id>/like/', login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.LIKE)),
        name='question_like'),
    path('<int:question_id>/dislike/', login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.DISLIKE)),
        name='question_dislike'),

    path('<int:question_id>/top/', views.make_top, name='make_top'),
]





