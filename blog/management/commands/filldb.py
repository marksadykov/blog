from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from blog.models import Question, Answer, Profile
from random import choice
from faker import Faker
from taggit.models import Tag

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
           user =  User.objects.create(password=f.password(), username=f.name(), email=f.email())
           user.save()
           profile = Profile.objects.create(user=user)
           profile.save()

    def fill_questions(self, cnt):
        tags = ['awesome', 'wow', 'cool', 'worst', 'sometag', 'helpme', 'onemore']
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        for i in range(cnt):
            q = Question.objects.create(
                author_id=User.objects.get(id=choice(author_ids)),
                question_title=f.sentence()[:128],
                article_text=f.sentence()[:256],
                pub_date=timezone.now()
            )
            for _ in range(f.random_int(min=2, max=5)):
                 q.tags.add(tags[f.random_int(min=0, max=3)])


    def fill_answers(self, cnt):
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Answer.objects.create(
                author_id=User.objects.get(id=choice(author_ids)),
                question=Question.objects.get(id=choice(questions_ids)),
                text=f.sentence()[:256],
            )


    def handle(self, *args, **options):
        self.fill_authors(options.get('authors', 0))
        self.fill_questions(options.get('questions', 0))
        self.fill_answers(options.get('answers', 0))