from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.db.models import Sum
from taggit.managers import TaggableManager

from django.contrib.auth.models import User

import PIL
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill
 

class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
 
    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)
 
    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
 
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
 
    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete = models.CASCADE)
 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
 
    objects = LikeDislikeManager()


class Question(models.Model):
	question_title = models.CharField('заголовок вопроса', max_length=200)
	article_text = models.TextField('текст вопроса')
	author_id = models.ForeignKey(User, on_delete = models.CASCADE)
	votes = GenericRelation(LikeDislike, related_query_name='questions')
	pub_date = models.DateTimeField('дата публикации')
	tags = TaggableManager()
	id_top_answer = models.IntegerField('id лучшего ответа', default = -1)

	def new_questions(self):
		return self.pub_date >= (timezone.now() - datetime.timedelta(days=1))

	def questions(self):
		return self.get_queryset().filter(content_type__model='question').order_by('-questions__pub_date')


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	author_id = models.ForeignKey(User, on_delete = models.CASCADE)
	answer_text = models.CharField('текст ответа', max_length = 200)



class Profile(models.Model):
     user = models.OneToOneField(User, on_delete = models.CASCADE)
     img = models.ImageField(default = 'default.jpg', upload_to = 'user_images')
