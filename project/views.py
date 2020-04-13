from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import *

# These methods are all for opening a template and passing it arguments


def login_signup(request):
	context = {}
	return render(request, 'project/login_signup.html', context)


def login(request):
	context = {}
	return render(request, 'project/login.html', context)


# Build the signup screen. This will also add the user to the database if they are approved
def signup(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = UserForm(request.POST)
		# check whether it's valid. this just checks if the fields are filled out
		if form.is_valid():
			new_user = form.save()
			qs = User.objects.all().values()
			print(qs)
			# TODO figure out how to change the url to a new one
			return HttpResponseRedirect('/home/')
			# return render(request, 'project/home.html', {})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = UserForm
	return render(request, 'project/signup.html', {'form': form})


def home(request):
	context = {
		# Put dictionary values in here as needed
	}
	return render(request, 'project/home.html', context)
