from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'project'
urlpatterns = [
	# TODO the order of these matter, do specific -> general
	# Empty path
	path('', views.login_signup, name='login_signup'),
	# localhost/signup
	path('signup/', views.signup, name='signup'),
	# localhost/login (login screen)
	path('login/', views.login, name='login'),
	# localhost/home/Username
	path('home/<slug:username>/', views.home, name='home'),
	# localhoust/home/addcity
	# path('home/<slug:username>/addcity/', views.add_city, name='add_city'),

	# TODO DELETE THIS IS FOR TEST
	# path('name/', views.get_name, name='get_name'),
]
