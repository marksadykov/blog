from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Answer, LikeDislike

from taggit.models import Tag

from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from django.utils import timezone

from django import forms

from taggit.forms import *


class add_post(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ['votes', 'pub_date', 'author_id', 'id_top_answer']		

	question_title = forms.CharField(label='Заголовок вопроса', widget=forms.TextInput(attrs={'class': 'form-control'}))
	article_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),label='Текст вопроса')
	tags = TagField(label='Теги', widget=forms.TextInput(attrs={'class': 'form-control'}))