from django.urls import path

from . import views

urlpatterns = [
	# Empty path
	path('', views.login_signup, name='login_signup'),
	# localhost/signup
	path('signup/', views.signup, name='signup'),
	# homescreen / main screen
	path('home', views.home, name='home'),
]
