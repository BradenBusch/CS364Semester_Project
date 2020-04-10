from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import NameForm
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


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return render(request, 'project/home.html')
	else:
		form = UserCreationForm()
	return render(request, 'project/signup.html', {'form': form})


def home(request):
	context = {
		# Put dictionary values in here as needed
	}
	# TODO get data from the FORM class.
	# This will only work if the data is posted. if a guest signed in it wouldnt work
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	print(f'Name: {firstname} {lastname}')
	return render(request, 'project/home.html', context)


def get_name(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			# can use the forms cleaned_data attribute to update database before doing redirect
			# TODO so i think i would pass the data here to a new page (somehow)
			return HttpResponseRedirect('/project/')

		# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
	return render(request, 'project/name.html', {'form': form})
	# form = UserCreationForm
	# return render(request, "project/name.html", {'form': form})
