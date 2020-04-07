from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import *

# These methods are all for opening a template and passing it arguments


def login_signup(request):
	context = {
		# Put dictionary values in here as needed
	}
	return render(request, 'project/login_signup.html', context)


def signup(request):
	context = {
		# Put dictionary values in here as needed
	}
	return render(request, 'project/signup.html', context)


def home(request):
	context = {
		# Put dictionary values in here as needed
	}
	return render(request, 'project/home.html', context)
