from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
	# Empty path
	path('', views.login_signup, name='login_signup'),
	# localhost/signup
	path('signup/', views.signup, name='signup'),
	# localhost/login (login screen)
	path('login/', views.login, name='login'),
	# localhost/home/Username
	path('home/<slug:username>/', views.home, name='home'),
	# localhost/home/Username/explore
	path('home/<slug:username>/explore', views.explore, name='explore'),
]
