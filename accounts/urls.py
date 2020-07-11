from django.urls import path
from . import views

from django.conf.urls import url

from django.contrib.auth.models import User

app_name = 'accounts'
urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
	path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
