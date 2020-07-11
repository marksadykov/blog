from django.contrib import admin
from .models import Question, Answer, LikeDislike, Profile

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LikeDislike)
admin.site.register(Profile)