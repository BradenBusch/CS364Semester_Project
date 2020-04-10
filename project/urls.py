from django.urls import path

from . import views

urlpatterns = [
	# Empty path
	path('', views.login_signup, name='login_signup'),
	# localhost/signup
	path('signup/', views.signup, name='signup'),
	# localhost/login (login screen)
	path('login/', views.login, name='login'),
	# localhost/home (homescreen / main screen)
	path('home/', views.home, name='home'),
	# TODO DELETE THIS IS FOR TEST
	path('name/', views.get_name, name='get_name'),
]
