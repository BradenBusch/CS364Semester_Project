from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import *
from . import constants
from django.views.decorators.csrf import ensure_csrf_cookie


def login_signup(request):
	# Upon start, store locations. Don't do this again unless db is dropped
	# If you drop all tables, you need to change constants.STORE_LOCATIONS back to True
	if constants.STORE_LOCATIONS is True:
		constants.store_locations()
	if constants.STORE_ARTISTS is True:
		constants.store_artists()
	q = Location.objects.all().values()
	print(q)
	q = list(Artist.objects.all().values())
	print(q)
	context = {}
	return render(request, 'project/login_signup.html', context)


# TODO Will have to write my own authentication here i suppose
def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = LoginForm(request.POST)
		# check whether it's valid. this just checks if the fields are filled out
		if form.is_valid():
			try:
				user = User.objects.get(username=form.cleaned_data['username'])
			except User.DoesNotExist:
				return HttpResponseRedirect('/login/')
			if user.password == form.cleaned_data['password']:
				username = form.cleaned_data['username']
				return HttpResponseRedirect('/home/' + username + '/')
				# return render(request, 'project/home.html', {'user'})
			else:
				return HttpResponseRedirect('/login/')
				# return render(request, 'project/home.html', {})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = LoginForm()
	return render(request, 'project/login.html', {'form': form})


# Build the signup screen. This will also add the user to the database if they are approved
def signup(request):
	print('hello')
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = UserForm(request.POST)
		# check whether it's valid. this just checks if the fields are filled out
		if form.is_valid():
			try:
				user = User.objects.get(username=form.cleaned_data['username'])
			except User.DoesNotExist:
				new_user = form.save(commit=False)
				# TODO put the foreign key for location here
				# TODO get the id of the location with the city and state the user selected, then make that the foreign
				new_user.password = form.cleaned_data['confirm_password']
				selected_city = request.POST['selectedCity']
				user_loc = Location.objects.get(city=selected_city)
				new_user.location = user_loc
				new_user.save()
				qs = User.objects.all().values()
				print(qs)
				return HttpResponseRedirect('/login/')
				# return render(request, 'project/home.html', {})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = UserForm()
	context = {
		'form': form,
		'states': states,
		'cities': cities,
	}
	return render(request, 'project/signup.html', context)


# Add a state/city to the locations model. #TODO delete?
def add_city(request, username=None):
	# This method will always start as a post
	if request.method == 'POST':
		form = StateForm(request.POST)
		context = {
			'form': form,
			'username': username
		}
		if form.is_valid():
			# TODO database updates in here. Check if user already has location, if not update
			print(username)
		return render(request, 'project/addcity.html', context)


def home(request, username=None):
	# TODO get all information to display in the HTML of the home screen here
	user = User.objects.get(username=username)
	user_state = user.location.state
	user_city = user.location.city
	artists = None
	if request.method == 'POST' and request.is_ajax:
		artist_id = request.POST.get('artist_id', None)
		search_res = request.POST.get('search_bar', None)
		if artist_id is not None:
			# Check if user is already following artist
			# TODO delete this if statement
			#  after the subquery from ^ is working
			if not user.artist_set.filter(artist_id=artist_id).exists():
				artist = Artist.objects.get(artist_id=artist_id)
				artist.users.add(user)
				print(f'artist {artist.artist_name} users: {list(artist.users.all().values())}')
				print(f'user id: {user.user_id} artists: {list(user.artist_set.all().values())}')
		# use like and order by
		# SELECT artist_name
		#       FROM (subquery checking if user already has this artist)
		#       WHERE artist_name LIKE "{search_res} %"
		#       ORDER BY artist_name
		# TODO this could probably be a subquery. We should't show artists were already tracking
		if search_res is not None:
			artists = Artist.objects.filter(artist_name__startswith=search_res).order_by('artist_name')

	print(f'Username: {username}\nUser State: {user_state}\nUser City: {user_city}')

	context = {
		'user': user,
		'artists': artists,
	}
	return render(request, 'project/home.html', context)
